"""
This creates a venv and and build a project that consumes our SDK and check that we can import it correctly.
"""

import pytest

from pathlib import Path
from .venv import VEnv

@pytest.mark.sdk
def test_build_module(virtualenv: VEnv, curdir: Path, tmp_path: Path):
    # To enable current project to be used we have to cut pypi index
    # But doing so would cause issues with dependencies, so we use the
    # pip wheel command to download all needed wheels from pypi and
    # put them in a temporary index.
    virtualenv.module("pip", "wheel",
        "scikit-build-core",
        "ninja",
        "cmake",
        "vtk-sdk-python-wheel-helper",
        "vtk-sdk==9.6.0",
        "slicer-core==5.11.0.*",
        "slicer-core-sdk==5.11.0.*",
        "--extra-index-url", "https://vtk.org/files/wheel-sdks",
       "--wheel-dir", tmp_path.as_posix()
    )

    runtime_dir = curdir.parent.resolve()
    virtualenv.module("pip", "wheel", runtime_dir.as_posix(),
        "--find-links", tmp_path.as_posix(),
        "--no-index",
        "--wheel-dir", tmp_path.as_posix()
    )

    sdk_dir = (curdir.parent.parent / "LayerDMSDK").resolve()
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
