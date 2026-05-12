from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def login(email, password):

    response = client.post(
        "/login",
        json={
            "email": email,
            "password": password
        }
    )

    print("\nSTATUS:", response.status_code)
    print("RESPONSE:", response.json())

    return response.json()["access_token"]