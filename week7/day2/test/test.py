from fastapi.testclient import TestClient
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from main import app

client = TestClient(app)

def test_docs():
    response = client.get("/docs")
    assert response.status_code == 200