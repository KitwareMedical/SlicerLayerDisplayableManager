#!/usr/bin/env python3
"""Pin the slicer-core version a wheel is built against.

"""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACKAGES = ("LayerDM", "LayerDMSDK")
VERSION_TAG = "refs/tags/v[0-9]*"


def library_version() -> str:
    tag = subprocess.run(
        [
            "git",
            "for-each-ref",
            "--sort=-v:refname",
            "--count=1",
            "--format=%(refname:strip=2)",
            VERSION_TAG,
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if not tag:
        raise SystemExit(
            f"error: no v<major>.<minor>.<patch> tag found in {ROOT} "
            "(shallow clone without tags? use fetch-depth: 0)"
        )
    return tag.removeprefix("v")


def runtime_requirement(slicer_core: str) -> str:
    """slicer-core requirement covering every build revision of the same ABI.

    5.11.0.6 -> "slicer-core==5.11.0.*" (matches 5.11.0.0 ... 5.11.0.255)
    """
    abi = ".".join(slicer_core.split(".")[:3])
    return f"slicer-core=={abi}.*"


def pin(package: str, slicer_core: str, version: str) -> None:
    path = ROOT / package / "pyproject.toml"
    text = path.read_text(encoding="utf-8")
    runtime = runtime_requirement(slicer_core)

    text, build_pins = re.subn(
        r"slicer-core-sdk==[^\"\n]+", f"slicer-core-sdk=={slicer_core}", text
    )
    text, runtime_pins = re.subn(
        r"\"slicer-core==[^\"\n]+\"", f'"{runtime}"', text
    )
    text, dynamic = re.subn(
        r"^dynamic = \[\"version\"\]$", f'version = "{version}"', text, flags=re.MULTILINE
    )
    text = re.sub(r"^metadata\.version\.provider[^\n]*\n", "", text, flags=re.MULTILINE)

    expected_runtime = 1 if package == "LayerDM" else 0
    if (runtime_pins, dynamic) != (expected_runtime, 1) or build_pins < 1:
        raise SystemExit(
            f"error: unexpected content in {path} "
            f"(slicer-core-sdk pins: {build_pins}, "
            f"slicer-core dependencies: {runtime_pins} (expected {expected_runtime}), "
            f"dynamic version: {dynamic})"
        )

    path.write_text(text, encoding="utf-8")
    print(f"{path.relative_to(ROOT)}: version={version} build={slicer_core} runtime={runtime}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--slicer-core",
        required=True,
        help="slicer-core version to build against, e.g. 5.11.0.6",
    )
    args = parser.parse_args()

    if not re.fullmatch(r"\d+(\.\d+)+", args.slicer_core):
        raise SystemExit(f"error: not a valid slicer-core version: {args.slicer_core}")

    version = f"{library_version()}.{args.slicer_core}"
    for package in PACKAGES:
        pin(package, args.slicer_core, version)
    print(f"wheel version: {version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
