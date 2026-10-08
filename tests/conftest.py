import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
os.environ["LLM_PROVIDER"] = "fake"  # las pruebas nunca llaman a una API externa


@pytest.fixture(scope="session")
def assistant():
    from assistant.service import Assistant

    return Assistant()
