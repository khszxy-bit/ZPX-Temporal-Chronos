"""Optional, small local timing comparison. NOT an apples-to-apples EDR test.

Copyright (c) 2026 Space Analysis (우주분석) / ZPX research contributors.
SPDX-License-Identifier: MIT
"""

import json
import platform
import statistics
from time import perf_counter_ns

from zpx_open_core import atlas, root_for_files


def median_us(fn, repeats: int) -> float:
    durations = []
    for _ in range(repeats):
        start = perf_counter_ns()
        fn()
        durations.append((perf_counter_ns() - start)/1000)
    return round(statistics.median(durations), 2)


def benchmark() -> dict:
    results = []
    for size in (250, 4096):
        data = bytes(range(256))*(size//256) + bytes(range(size % 256))
        files = {"data/synthetic.bin": data}
        results.append({
            "payload_bytes": size,
            "merkle_root_us_median_20": median_us(lambda: root_for_files(files), 20),
            "exact_17bit_atlas_us_median_10": median_us(lambda: atlas(data, 17), 10),
            "remark": "Different workloads. Atlas returns many exact coordinate points."
        })
    return {
        "machine": platform.platform(), "python": platform.python_version(),
        "measurements": results,
        "scope": "Python local timings; no actual security filtering or throughput claim",
    }


if __name__ == "__main__":
    print(json.dumps(benchmark(), ensure_ascii=False, indent=2))
