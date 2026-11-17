"""Opt-in READ-ONLY directory-integrity CLI for ZPX Chronos-Shield v8.

Python >=3.10 / stdlib. This is NOT antivirus, file interception, a firewall,
or a secure monitor against an attacker who controls this host and HMAC key.
No files in the monitored directory are modified by this program.
It uses MIT-licensed zpx_open_core.py in the same folder.

Copyright (c) 2026 Space Analysis (우주분석) / ZPX research contributors.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
from pathlib import Path
import secrets
import sys

from zpx_open_core import canonical_json, root_from_records


SCHEMA = "ZPX-CHRONOS-v8-READ-ONLY"


def hash_one_file(filename: Path) -> dict[str, int | str]:
    if filename.is_symlink():
        raise ValueError(f"Symlink is not monitored: {filename}")
    before = filename.stat()
    if not filename.is_file():
        raise ValueError(f"Not a regular file: {filename}")
    h = hashlib.sha256()
    with filename.open("rb") as stream:
        while True:
            chunk = stream.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    after = filename.stat()
    if ((before.st_size, before.st_mtime_ns, before.st_ino)
            != (after.st_size, after.st_mtime_ns, after.st_ino)):
        raise RuntimeError(f"Concurrent file change during scan: {filename}")
    return {"bytes": after.st_size, "sha256": h.hexdigest()}


def directory_records(root: Path) -> dict[str, dict]:
    if root.is_symlink() or not root.is_dir():
        raise ValueError("Provide an existing real directory, not a symlink")
    items: dict[str, dict] = {}
    for directory, subdirs, names in os.walk(root, followlinks=False):
        for subdir in subdirs:
            if (Path(directory) / subdir).is_symlink():
                raise ValueError("Monitored tree contains a symlink directory")
        subdirs.sort()
        for filename in sorted(names):
            full = Path(directory) / filename
            if full.is_symlink():
                raise ValueError("Monitored tree contains a symlink file")
            name = full.relative_to(root).as_posix()
            items[name] = hash_one_file(full)
    return dict(sorted(items.items()))


def _ensure_external(root: Path, dest: Path) -> None:
    resolved_root = root.resolve()
    if dest.resolve().is_relative_to(resolved_root):
        raise ValueError("Manifest and key must be OUTSIDE the monitored directory")


def _create_private_file(path: Path, payload: bytes) -> None:
    # O_EXCL avoids silently overwriting any existing user file.
    descriptor = os.open(str(path), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    with os.fdopen(descriptor, "wb") as stream:
        stream.write(payload)


def write_baseline(root: Path, manifest: Path, keyfile: Path) -> dict:
    _ensure_external(root, manifest)
    _ensure_external(root, keyfile)
    if manifest.resolve() == keyfile.resolve():
        raise ValueError("Manifest and key paths must differ")
    if manifest.exists() or keyfile.exists():
        raise FileExistsError("Refusing to overwrite an existing manifest/key")
    records = directory_records(root)
    body = {"schema": SCHEMA, "files": records,
            "root": root_from_records(records)}
    secret = secrets.token_bytes(32)
    tag = hmac.new(secret, canonical_json(body), hashlib.sha256).hexdigest()
    signed = {**body, "hmac_sha256": tag}
    _create_private_file(keyfile, secret)
    _create_private_file(manifest, canonical_json(signed) + b"\n")
    return {"action": "init", "files": len(records), "root": body["root"],
            "note": "Local baseline; move protected key/logs to independent security domain"}


def check_baseline(root: Path, manifest: Path, keyfile: Path) -> tuple[int, dict]:
    _ensure_external(root, manifest)
    _ensure_external(root, keyfile)
    signed = json.loads(manifest.read_text(encoding="utf-8"))
    secret = keyfile.read_bytes()
    if len(secret) < 32 or signed.get("schema") != SCHEMA:
        raise ValueError("Unrecognized baseline or invalid key")
    tag = signed.get("hmac_sha256")
    if not isinstance(tag, str):
        raise ValueError("Manifest HMAC tag is missing")
    body = {key: signed[key] for key in ("schema", "files", "root")}
    expected = hmac.new(secret, canonical_json(body), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(tag, expected):
        raise ValueError("Manifest authentication FAILED")
    if root_from_records(body["files"]) != body["root"]:
        raise ValueError("Stored manifest Merkle root FAILED")
    current = directory_records(root)
    previous = body["files"]
    added = sorted(set(current) - set(previous))
    deleted = sorted(set(previous) - set(current))
    modified = sorted(path for path in set(previous) & set(current)
                      if previous[path] != current[path])
    same = not (added or deleted or modified)
    return (0 if same else 2), {
        "action": "check", "clean": same,
        "approved_root": body["root"],
        "observed_root": root_from_records(current),
        "added": added, "deleted": deleted, "modified": modified,
        "note": "Observation only. There is NO automatic block/quarantine."
    }


def cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("init", "check"):
        sub = commands.add_parser(name)
        sub.add_argument("--directory", type=Path, required=True)
        sub.add_argument("--manifest", type=Path, required=True)
        sub.add_argument("--keyfile", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            message = write_baseline(args.directory, args.manifest, args.keyfile)
            status = 0
        else:
            status, message = check_baseline(args.directory, args.manifest,
                                             args.keyfile)
        print(json.dumps(message, ensure_ascii=False, indent=2))
        return status
    except (OSError, ValueError, RuntimeError, KeyError, TypeError,
            json.JSONDecodeError) as exc:
        print(json.dumps({"status": "ERROR", "description": str(exc)},
                         ensure_ascii=False), file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(cli())
