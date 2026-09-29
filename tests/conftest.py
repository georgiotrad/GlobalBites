import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture()
def client(tmp_path, monkeypatch):
    db_path = tmp_path / "test-globalbites.db"
    monkeypatch.setenv("GLOBALBITES_DB_PATH", str(db_path))
    monkeypatch.setenv("SEED_DEMO_USERS", "1")
    monkeypatch.setenv("SECRET_KEY", "test-secret")
    monkeypatch.delenv("GLOBALBITES_ML_FORCE_FAILURE", raising=False)
    from app.backend.app import create_app
    app = create_app({"TESTING": True, "SECRET_KEY": "test-secret"})
    return app.test_client()
