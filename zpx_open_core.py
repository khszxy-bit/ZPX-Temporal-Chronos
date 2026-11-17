"""ZPX Chronos-Shield v8 — MIT-licensed defensive research skeleton.

An integer-only / Fraction-exact three-level spatial atlas and a toy
authenticated timeline. It contains NO OS write prevention or antivirus.
Python >=3.10, standard library only. Safe to run on synthetic data.

Copyright (c) 2026 Space Analysis (우주분석) / ZPX research contributors.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from fractions import Fraction
from hashlib import sha256
import hmac
import json
import secrets
from typing import Mapping


L1_BITS = 17
L2_BITS = 17 * 17
SPHERE_SCALE = 5


def bits_of(payload: bytes) -> tuple[int, ...]:
    return tuple((octet >> shift) & 1 for octet in payload
                 for shift in range(7, -1, -1))


def signed_code(bits: tuple[int, ...]) -> int:
    if any(bit not in (0, 1) for bit in bits):
        raise ValueError("Only binary digits are allowed")
    raw = sum(bit << shift for shift, bit in enumerate(bits))
    return raw - (1 << len(bits)) if bits and raw >= (1 << (len(bits) - 1)) else raw


def decode_signed(value: int, width: int) -> tuple[int, ...]:
    if width < 0:
        raise ValueError("Invalid width")
    raw = value % (1 << width) if width else 0
    return tuple((raw >> shift) & 1 for shift in range(width))


@dataclass(frozen=True)
class SpatialCell:
    width: int
    vector_a: tuple[int, int, int]
    vector_b: tuple[int, int, int]
    vector_c: tuple[int, int, int]
    geometric_volume: int
    one_third_volume: Fraction
    sphere: tuple[Fraction, Fraction, Fraction]


def encode_cell(bits: tuple[int, ...], scale: int = SPHERE_SCALE) -> SpatialCell:
    """Two vectors -> orthogonal third vector -> exact S²(Q) sphere.

    Does not label an input as safe or malicious; every bit pattern satisfies
    the same 90-degree and one-third relationships.
    """
    if not bits or scale <= 0:
        raise ValueError("Nonempty cell and a positive scale required")
    split = (len(bits) + 1) // 2
    x, y = signed_code(bits[:split]), signed_code(bits[split:])
    a, b, c = (1, x, 0), (0, 1, y), (x*y, -y, 1)
    assert sum(a[i]*c[i] for i in range(3)) == 0
    assert sum(b[i]*c[i] for i in range(3)) == 0
    d = sum(v*v for v in c)
    denominator = scale*scale + x*x + y*y
    point = (Fraction(2*scale*x, denominator),
             Fraction(2*scale*y, denominator),
             Fraction(x*x+y*y-scale*scale, denominator))
    assert sum(v*v for v in point) == 1
    return SpatialCell(len(bits), a, b, c, d, Fraction(d, 3), point)


def inverse_cell(cell: SpatialCell, scale: int = SPHERE_SCALE) -> tuple[int, ...]:
    """Invert the sphere to the exact source bits using stored cell width."""
    X, Y, Z = cell.sphere
    if Z == 1:
        raise ValueError("Infinite point cannot encode a finite bit cell")
    x, y = scale*X/(1-Z), scale*Y/(1-Z)
    if x.denominator != 1 or y.denominator != 1:
        raise ValueError("The coordinates did not encode an integer pair")
    split = (cell.width + 1) // 2
    return decode_signed(int(x), split) + decode_signed(int(y), cell.width-split)


def atlas(payload: bytes, width: int) -> tuple[SpatialCell, ...]:
    """Keep cell order and variable last-cell width: no lossy compression."""
    if width <= 0:
        raise ValueError("Positive cell width required")
    binary = bits_of(payload)
    cells = tuple(encode_cell(binary[k:k+width])
                  for k in range(0, len(binary), width))
    recovered = tuple(bit for cell in cells for bit in inverse_cell(cell))
    assert recovered == binary
    return cells


def three_sphere_atlas(payload: bytes) -> dict[str, tuple[SpatialCell, ...]]:
    total = len(payload)*8
    return {
        "local_17": atlas(payload, L1_BITS),
        "middle_289": atlas(payload, L2_BITS),
        "whole_file": atlas(payload, max(1, total)),
    }


def sha(data: bytes) -> bytes:
    return sha256(data).digest()


def canonical_json(data: object) -> bytes:
    return json.dumps(data, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def file_record(path: str, payload: bytes) -> dict[str, int | str]:
    return {"bytes": len(payload), "sha256": sha(payload).hex()}


def records_for_files(files: Mapping[str, bytes]) -> dict[str, dict]:
    return {p: file_record(p, files[p]) for p in sorted(files)}


def root_from_records(records: Mapping[str, Mapping]) -> str:
    """Path- and length-bound SHA-256 Merkle commitment to a finite atlas.

    A 256-bit digest is not mathematically injective for arbitrary data;
    its practical integrity role relies on cryptographic assumptions.
    """
    if not records:
        return sha(b"ZPX8-EMPTY-ROOT\0").hex()
    leaves = []
    for path in sorted(records):
        name = path.encode("utf-8")
        record = records[path]
        content_hash = bytes.fromhex(record["sha256"])
        size = int(record["bytes"])
        if len(content_hash) != 32 or size < 0:
            raise ValueError("Malformed record")
        leaf = sha(b"ZPX8-LEAF\0" + len(name).to_bytes(4, "big") + name
                   + size.to_bytes(8, "big") + content_hash)
        leaves.append(leaf)
    layer = leaves
    while len(layer) > 1:
        paired = []
        for k in range(0, len(layer), 2):
            right = (layer[k+1] if k+1 < len(layer)
                     else sha(b"ZPX8-NO-RIGHT\0"))
            paired.append(sha(b"ZPX8-NODE\0" + layer[k] + right))
        layer = paired
    return sha(b"ZPX8-ROOT\0" + len(leaves).to_bytes(8, "big")
               + layer[0]).hex()


def root_for_files(files: Mapping[str, bytes]) -> str:
    return root_from_records(records_for_files(files))


@dataclass(frozen=True)
class LedgerEvent:
    seq: int
    minute: int
    action: str
    path: str
    outcome: str
    before: str
    after: str
    previous_mac: str
    mac: str


class ChronosGuard:
    """Toy ingress/egress and temporal HMAC ledger, NOT an OS policy engine.

    Role strings are unverified caller input. To build a real product, use an
    independent identity provider, mandatory OS enforcement and off-host keys.
    """

    def __init__(self, initial: Mapping[str, bytes], key: bytes | None = None):
        self.files = dict(initial)
        self.key = key if key is not None else secrets.token_bytes(32)
        if len(self.key) < 32:
            raise ValueError("A 32-byte or longer HMAC key is required")
        self.root = root_for_files(self.files)
        self.events: list[LedgerEvent] = []
        self.pinned_tip = "GENESIS"
        self.used_nonces: set[str] = set()
        self._log(0, "INSTALL", "*", "BASELINE", self.root, self.root)

    @staticmethod
    def event_body(event: LedgerEvent) -> bytes:
        data = asdict(event)
        data.pop("mac")
        return canonical_json(data)

    def _log(self, minute: int, action: str, path: str, outcome: str,
             before: str, after: str) -> None:
        if self.events and minute < self.events[-1].minute:
            raise ValueError("Simulated minute cannot decrease")
        prev = self.events[-1].mac if self.events else "GENESIS"
        item = LedgerEvent(len(self.events), minute, action, path, outcome,
                           before, after, prev, "")
        item = replace(item, mac=hmac.new(self.key, self.event_body(item),
                                         sha256).hexdigest())
        self.events.append(item)
        self.pinned_tip = item.mac

    def verify_events(self, events: list[LedgerEvent] | None = None) -> bool:
        events = self.events if events is None else events
        if not events or events[-1].mac != self.pinned_tip:
            return False
        previous = "GENESIS"
        minute = -1
        for sequence, item in enumerate(events):
            if (item.seq != sequence or item.previous_mac != previous
                    or item.minute < minute):
                return False
            expected = hmac.new(self.key, self.event_body(item), sha256).hexdigest()
            if not hmac.compare_digest(item.mac, expected):
                return False
            previous, minute = item.mac, item.minute
        return True

    @staticmethod
    def policy(path: str, role: str, release: bool) -> bool:
        if path.startswith("core/"):
            return role == "release_admin" and release
        if path.startswith("data/"):
            return role in ("operator", "release_admin")
        return False

    def change(self, minute: int, action: str, path: str, role: str,
               payload: bytes | None = None, destination: str | None = None,
               approved_release: bool = False) -> bool:
        if not self.verify_events():
            return False
        before = root_for_files(self.files)
        permitted = (before == self.root
                     and self.policy(path, role, approved_release))
        if action == "ADD":
            permitted &= path not in self.files and payload is not None
        elif action == "MODIFY":
            permitted &= path in self.files and payload is not None
        elif action == "DELETE":
            permitted &= path in self.files
        elif action == "MOVE":
            permitted &= (destination is not None
                          and self.policy(destination, role, approved_release)
                          and path in self.files and destination not in self.files)
        else:
            raise ValueError("Unknown action")
        if permitted:
            if action == "DELETE":
                self.files.pop(path)
            elif action == "MOVE":
                self.files[destination] = self.files.pop(path)
            else:
                self.files[path] = payload
            self.root = root_for_files(self.files)
        after = root_for_files(self.files)
        self._log(minute, action, path, "ALLOW" if permitted else "DENY",
                  before, after)
        return bool(permitted)

    def scan(self, minute: int) -> bool:
        if not self.verify_events():
            return False
        observed = root_for_files(self.files)
        clean = hmac.compare_digest(self.root, observed)
        self._log(minute, "SCAN", "*", "CLEAN" if clean else "ALERT",
                  self.root, observed)
        return clean

    def _egress_token(self, path: str, destination: str, nonce: str) -> str:
        data = self.files.get(path)
        if data is None:
            return ""
        material = canonical_json({"path": path, "recipient": destination,
                                   "nonce": nonce, "root": self.root,
                                   "sha256": sha(data).hex()})
        return hmac.new(self.key, b"ZPX8-EGRESS\0"+material, sha256).hexdigest()

    def issue_egress_token(self, path: str, destination: str,
                           nonce: str, role: str) -> str | None:
        if (role not in {"backup_service", "auditor"} or not destination
                or not nonce or nonce in self.used_nonces
                or path not in self.files or not self.verify_events()
                or self.root != root_for_files(self.files)):
            return None
        return self._egress_token(path, destination, nonce)

    def egress(self, minute: int, path: str, destination: str,
               nonce: str | None, token: str | None) -> bool:
        if not self.verify_events():
            return False
        permitted = bool(destination and nonce and token
                         and nonce not in self.used_nonces
                         and path in self.files
                         and self.root == root_for_files(self.files))
        if permitted:
            permitted = hmac.compare_digest(
                token, self._egress_token(path, destination, nonce))
        if permitted:
            self.used_nonces.add(nonce)
        self._log(minute, "EGRESS", path, "ALLOW" if permitted else "DENY",
                  self.root, self.root)
        return bool(permitted)


def demo() -> dict:
    """A reproducible toy run. Demo HMAC key must NEVER be deployed."""
    initial = {"core/engine.bin": bytes([0xA5])*250,
               "data/initial.txt": b"initial"}
    secret = sha(b"ZPX-V8-SYNTHETIC-TEST-KEY-NOT-FOR-REAL-USE")
    guard = ChronosGuard(initial, secret)
    result = {
        "initial_250byte_atlas_counts": [len(items) for items in
                                         three_sphere_atlas(initial["core/engine.bin"]).values()],
        "authorized_add": guard.change(1, "ADD", "data/now.log", "operator", b"new"),
        "authorized_move": guard.change(2, "MOVE", "data/now.log", "operator",
                                        destination="data/archive.log"),
        "unauthorized_core_add": guard.change(3, "ADD", "core/implant", "visitor", b"bad"),
        "scan_after_approved_changes": guard.scan(4),
        "egress_without_token": guard.egress(5, "data/initial.txt", "vault", "one", None),
    }
    token = guard.issue_egress_token("data/initial.txt", "vault", "one", "backup_service")
    result["valid_egress_token"] = guard.egress(6, "data/initial.txt", "vault", "one", token)
    result["egress_replay"] = guard.egress(7, "data/initial.txt", "vault", "one", token)
    guard.files["core/engine.bin"] = b"UNAPPROVED-CHANGE"
    result["scan_after_unapproved_change"] = guard.scan(8)
    result["ledger_valid"] = guard.verify_events()
    result["note"] = "Toy model only: no real filesystem or network interception"
    return result


if __name__ == "__main__":
    print(json.dumps(demo(), ensure_ascii=False, indent=2))
