from pathlib import Path
from .venv import VEnv

import pytest


@pytest.fixture(scope="session")
def curdir() -> Path:
    return Path(__file__).parent.resolve()


@pytest.fixture()
def virtualenv(tmp_path: Path) -> VEnv:
    """Temporary virtualenv for the test projects."""
    path = tmp_path / "venv"
    return VEnv(path)
