from fastapi.testclient import TestClient
from main import app
from tests.helper import login

client = TestClient(app)


# =========================
# ADMIN TESTS
# =========================

def test_admin_can_get_users():

    token = login("admin@test.com", "admin123")

    response = client.get(
        "/users",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    print("test_Admin_can_get_users PASSED")


def test_admin_can_delete_items():

    token = login("admin@test.com", "admin123")

    response = client.delete(
        "/items/1",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    # item may or may not exist
    assert response.status_code in [200, 404]
    print("test_admin_can_delete_items PASSED")


# =========================
# MANAGER TESTS
# =========================

def test_manager_cannot_get_users():

    token = login("manager@test.com", "manager123")

    response = client.get(
        "/users",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403
    print("test_manager_cannot_get_users PASSED")


def test_manager_can_create_category():

    token = login("manager@test.com", "manager123")

    response = client.post(
        "/categories",
        json={
            "name": "Electronics"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    # category may already exist
    assert response.status_code in [200, 400]
    print("test_manager_can_create_category PASSED")


def test_manager_cannot_delete_items():

    token = login("manager@test.com", "manager123")

    response = client.delete(
        "/items/1",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403
    print("test_manager_cannot_delete_items PASSED")


# =========================
# STAFF TESTS
# =========================

def test_staff_cannot_get_users():

    token = login("staff@test.com", "staff123")

    response = client.get(
        "/users",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403
    print("test_staff_cannot_get_users PASSED")


def test_staff_cannot_create_category():

    token = login("staff@test.com", "staff123")

    response = client.post(
        "/categories",
        json={
            "name": "Mobiles"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403
    print("test_staff_cannot_create_category PASSED")


def test_staff_cannot_create_item():

    token = login("staff@test.com", "staff123")

    response = client.post(
        "/categories/1/items",
        json={
            "name": "iPhone"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    # RBAC should block first
    assert response.status_code == 403
    print("test_staff_cannot_create_item PASSED")


# =========================
# UNAUTHORIZED TEST
# =========================

def test_no_token():

    response = client.get("/users")

    assert response.status_code == 422
    print("test_no_tokenPASSED")