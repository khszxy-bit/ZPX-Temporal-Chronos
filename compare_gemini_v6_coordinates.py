"""Independent reproduction of the v6 coordinate formula described in the paper.

Mathematical reconstruction, not a copy of the Gemini program or a claim of
an attack on any deployed server. Runs wholly on invented 16-byte inputs.

Copyright (c) 2026 Space Analysis (우주분석) / ZPX research contributors.
SPDX-License-Identifier: MIT
"""

import hashlib
import json
import random

from zpx_open_core import atlas, root_for_files


def reconstructed_v6_xy(path: str, content: bytes) -> tuple[int, int]:
    """Single-file case of the published accum_x/accum_y mod 1021/509."""
    content_part = int.from_bytes(hashlib.sha256(content).digest()[:4], "little")
    path_part = int.from_bytes(hashlib.sha256(path.encode()).digest()[:4], "little")
    x = ((content_part + len(content)) % 1021 - 510) or 1
    y = (((path_part ^ content_part) + 19) % 509 - 254) or -1
    return x, y


def reproduce() -> dict:
    path = "/data/test.db"
    rng = random.Random(1706)
    seen = {}
    for attempt in range(1, 15001):
        content = rng.getrandbits(128).to_bytes(16, "big")
        coordinate = reconstructed_v6_xy(path, content)
        earlier = seen.get(coordinate)
        if earlier is not None and earlier != content:
            a, b = {path: earlier}, {path: content}
            result = {
                "source": "Independently reconstructed Gemini v6 coordinate formula",
                "seed": 1706,
                "collision_at_sample": attempt,
                "same_compressed_xy": list(coordinate),
                "inputs_differ": earlier != content,
                "entire_sha256_differs": hashlib.sha256(earlier).digest() != hashlib.sha256(content).digest(),
                "v8_merkle_roots_differ": root_for_files(a) != root_for_files(b),
                "v8_reversible_17bit_cells_differ": atlas(earlier, 17) != atlas(content, 17),
                "scope": "Synthetic coordinate-collision demonstration, not real hacking",
            }
            assert result["v8_merkle_roots_differ"]
            assert result["v8_reversible_17bit_cells_differ"]
            return result
        seen[coordinate] = content
    raise RuntimeError("No collision found within the demonstration budget")


if __name__ == "__main__":
    print(json.dumps(reproduce(), ensure_ascii=False, indent=2))
