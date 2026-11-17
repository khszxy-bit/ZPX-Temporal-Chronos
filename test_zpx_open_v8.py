"""Reproducible standard-library-only tests for the MIT public skeleton.

All attack-like inputs are synthetic. No malware or network traffic is used.
"""

from __future__ import annotations

from dataclasses import replace
import hashlib
import json
from pathlib import Path
import random
import tempfile
import unittest

import zpx_open_core as core
import zpx_snapshot_cli as scanner
from compare_gemini_v6_coordinates import reproduce as reproduce_collision


SYNTHETIC_KEY = hashlib.sha256(b"ZPX-PUBLIC-V8-TEST-ONLY").digest()


class SpatialMathTests(unittest.TestCase):
    def test_independent_gemini_v6_collision_reference(self):
        comparison = reproduce_collision()
        self.assertEqual(comparison["collision_at_sample"], 442)
        self.assertEqual(comparison["same_compressed_xy"], [-50, -105])
        self.assertTrue(comparison["v8_merkle_roots_differ"])

    def test_three_sphere_counts_and_inverse(self):
        binary = bytes([0xA5])*250
        layers = core.three_sphere_atlas(binary)
        self.assertEqual([len(layer) for layer in layers.values()], [118, 7, 1])
        bits = core.bits_of(binary)
        for width, layer in zip((17, 289, 2000), layers.values()):
            self.assertEqual(tuple(v for c in layer for v in core.inverse_cell(c)), bits)
            for cell in layer:
                A, B, C = cell.vector_a, cell.vector_b, cell.vector_c
                self.assertEqual(sum(a*c for a, c in zip(A, C)), 0)
                self.assertEqual(sum(b*c for b, c in zip(B, C)), 0)
                self.assertEqual(cell.one_third_volume / cell.geometric_volume,
                                 core.Fraction(1, 3))
                self.assertEqual(sum(v*v for v in cell.sphere), 1)

    def test_all_131072_seventeen_bit_cells_are_reversible(self):
        """Exhaustive check of the entire finite 17-bit input domain."""
        visited = set()
        for n in range(1 << 17):
            bits = tuple((n >> j) & 1 for j in range(17))
            cell = core.encode_cell(bits)
            self.assertEqual(core.inverse_cell(cell), bits)
            visited.add(cell.sphere)
        self.assertEqual(len(visited), 1 << 17)

    def test_all_2000_single_bit_flips_change_a_local_cell(self):
        random_bits = core.bits_of(random.Random(20261117).randbytes(250))
        for changed_index in range(2000):
            begin = (changed_index // 17)*17
            reference = random_bits[begin:begin+17]
            mutated = list(reference)
            mutated[changed_index-begin] ^= 1
            self.assertNotEqual(core.encode_cell(reference).sphere,
                                core.encode_cell(tuple(mutated)).sphere)

    def test_volume_ratio_and_orthogonality_are_not_security_decisions(self):
        innocent = core.encode_cell((0,)*17)
        changed = core.encode_cell((1,)+(0,)*16)
        self.assertNotEqual(innocent.sphere, changed.sphere)
        self.assertEqual(innocent.geometric_volume, changed.geometric_volume)
        self.assertEqual(innocent.one_third_volume * 3,
                         innocent.geometric_volume)
        self.assertEqual(changed.one_third_volume * 3,
                         changed.geometric_volume)

    def test_path_move_and_same_size_change_affect_root(self):
        first = {"data/a.txt": b"AAAAAAAA"}
        changed = {"data/a.txt": b"BBBBBBBB"}
        moved = {"data/b.txt": b"AAAAAAAA"}
        self.assertNotEqual(core.root_for_files(first), core.root_for_files(changed))
        self.assertNotEqual(core.root_for_files(first), core.root_for_files(moved))


class TemporalPolicyTests(unittest.TestCase):
    def test_authorized_timeline_and_rejected_core_modification(self):
        baseline = {"core/main.bin": b"trusted", "data/old": b"log"}
        guard = core.ChronosGuard(baseline, SYNTHETIC_KEY)
        self.assertTrue(guard.change(1, "ADD", "data/new", "operator", b"added"))
        self.assertTrue(guard.change(2, "MOVE", "data/new", "operator", destination="data/archive"))
        self.assertTrue(guard.change(3, "DELETE", "data/archive", "operator"))
        self.assertFalse(guard.change(4, "ADD", "core/implant", "visitor", b"malware"))
        self.assertTrue(guard.scan(5))
        self.assertTrue(guard.verify_events())

    def test_persistent_changes_and_hmac_record_tampering(self):
        guard = core.ChronosGuard({"data/file": b"BASELINE"}, SYNTHETIC_KEY)
        guard.files["data/file"] = b"INJECTED"
        self.assertFalse(guard.scan(1))
        tampered = list(guard.events)
        tampered[1] = replace(tampered[1], minute=777)
        self.assertFalse(guard.verify_events(tampered))

    def test_egress_requires_valid_non_replayed_token(self):
        guard = core.ChronosGuard({"data/file": b"BASELINE"}, SYNTHETIC_KEY)
        self.assertFalse(guard.egress(1, "data/file", "vault", "nonce-1", None))
        token = guard.issue_egress_token("data/file", "vault", "nonce-1", "backup_service")
        self.assertTrue(guard.egress(2, "data/file", "vault", "nonce-1", token))
        self.assertFalse(guard.egress(3, "data/file", "vault", "nonce-1", token))
        self.assertFalse(guard.egress(4, "data/file", "vault", "nonce-2", "0"*64))

    def test_unobserved_transient_change_and_claimed_role_still_bypass(self):
        guard = core.ChronosGuard({"data/file": b"SAFE"}, SYNTHETIC_KEY)
        guard.files["data/file"] = b"BAD"
        guard.files["data/file"] = b"SAFE"
        self.assertTrue(guard.scan(1))  # The file was restored before inspection.
        self.assertTrue(guard.change(2, "MODIFY", "data/file", "operator", b"BAD"))
        # 'operator' is a raw caller-provided string, not an authenticated identity.


class ReadOnlyFilesystemTests(unittest.TestCase):
    def test_init_detect_restore_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as base:
            base_dir = Path(base)
            monitored = base_dir / "monitored"
            monitored.mkdir()
            target = monitored / "demo.txt"
            target.write_text("Hello", encoding="utf-8")
            manifest, key = base_dir / "baseline.json", base_dir / "key.bin"
            result = scanner.write_baseline(monitored, manifest, key)
            self.assertEqual(result["files"], 1)
            code, verified = scanner.check_baseline(monitored, manifest, key)
            self.assertEqual(code, 0)
            self.assertTrue(verified["clean"])
            target.write_text("World", encoding="utf-8")  # Same file size.
            code, modified = scanner.check_baseline(monitored, manifest, key)
            self.assertEqual(code, 2)
            self.assertEqual(modified["modified"], ["demo.txt"])
            target.write_text("Hello", encoding="utf-8")
            code, _ = scanner.check_baseline(monitored, manifest, key)
            self.assertEqual(code, 0)
            with self.assertRaises(FileExistsError):
                scanner.write_baseline(monitored, manifest, key)

    def test_manifest_tamper_and_manifest_inside_monitored_tree_rejected(self):
        with tempfile.TemporaryDirectory() as base:
            root = Path(base)
            monitored = root / "target"
            monitored.mkdir()
            (monitored / "file").write_bytes(b"ok")
            manifest, key = root / "state.json", root / "secret"
            scanner.write_baseline(monitored, manifest, key)
            parsed = json.loads(manifest.read_text(encoding="utf-8"))
            parsed["files"]["file"]["bytes"] = 999
            manifest.write_text(json.dumps(parsed), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "authentication FAILED"):
                scanner.check_baseline(monitored, manifest, key)
            with self.assertRaises(ValueError):
                scanner.write_baseline(monitored, monitored / "inside.json",
                                       root / "newkey.bin")


if __name__ == "__main__":
    unittest.main(verbosity=2)
