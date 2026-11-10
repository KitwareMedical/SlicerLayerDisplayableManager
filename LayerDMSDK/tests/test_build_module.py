"""
This creates a venv and builds a project that consumes our SDK and checks that we can import it correctly.

This tests the SDK from the point of view of a third party package building against it,
hence it is part of the SDK test suite and not of the LayerDM unittests.
"""

import re
from pathlib import Path

from .venv import VEnv


def slicer_pins(runtime_dir: Path) -> tuple[str, str]:
    """Return the (slicer-core, slicer-core-sdk) requirements the runtime declares.

    """
    pyproject = (runtime_dir / "pyproject.toml").read_text(encoding="utf-8")
    sdk = re.search(r'"slicer-core-sdk==([^"]+)"', pyproject)
    core = re.search(r'"slicer-core==([^"]+)"', pyproject)
    if sdk is None or core is None:
        raise AssertionError(f"no slicer-core pins found in {(runtime_dir / 'pyproject.toml')}")
    return f"slicer-core=={core.group(1)}", f"slicer-core-sdk=={sdk.group(1)}"


def test_build_module(virtualenv: VEnv, curdir: Path, tmp_path: Path):
    # To enable current project to be used we have to cut pypi index
    # But doing so would cause issues with dependencies, so we use the
    # pip wheel command to download all needed wheels from pypi and
    # put them in a temporary index.
    runtime_dir = (curdir.parent.parent / "LayerDM").resolve()
    slicer_core, slicer_core_sdk = slicer_pins(runtime_dir)

    virtualenv.module("pip", "wheel",
        "scikit-build-core",
        "ninja",
        "cmake",
        "setuptools-scm",
        "vtk-sdk-python-wheel-helper",
        "vtk-sdk==9.6.0",
        slicer_core,
        slicer_core_sdk,
        "--extra-index-url", "https://vtk.org/files/wheel-sdks",
       "--wheel-dir", tmp_path.as_posix()
    )

    virtualenv.module("pip", "wheel", runtime_dir.as_posix(),
        "--find-links", tmp_path.as_posix(),
        "--no-index",
        "--wheel-dir", tmp_path.as_posix()
    )

    sdk_dir = curdir.parent.resolve()
    virtualenv.module("pip", "wheel", sdk_dir.as_posix(),
        "--find-links", tmp_path.as_posix(),
        "--no-index",
        "--wheel-dir", tmp_path.as_posix()
    )

    test_dir = curdir / "packages" / "build_module"
    virtualenv.module("pip", "install", test_dir.as_posix(),
        "--find-links", tmp_path.as_posix(),
        "--no-index"
    )

    virtualenv.run("python", (test_dir / "main.py").as_posix())
