import pytest

pytestmark = pytest.mark.api

def test_get(api_client):
    response = api_client.get("/users")

    assert response.status_code == 200
    assert len(response.json()) > 0

@pytest.mark.parametrize("name,email,status", [
    ("Nguyen Minh Anh", "anh.nguyen@gmail.com", 201),
    ("Nguyen Van A", "a@example.com", 201),
    ("Tên_Có_Ký_Tự_@#$", "b@example.com", 200),
    ("User 3", "invalid-email", 400)
])
def test_post(api_client, name, email, status):
    payload = {
        "name": name,
        "email": email
    }

    response = api_client.post(endpoint="/users", payload=payload)
    assert response.status_code == status
    
    created_user = response.json() 
    assert created_user["name"] == name
    assert created_user["email"] == email

def test_delete(api_client):
    response = api_client.delete("/users", id = 1)
    assert response.status_code == 200

def test_put(api_client):
    payload = {
        "name": "Ky su SDET",
        "email": "anh.nguyenupdate@gmail.com"
    }

    response = api_client.put("/users", payload = payload, id = 1)
    
    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user["name"] == "Ky su SDET"
    assert updated_user["email"] == "anh.nguyenupdate@gmail.com"
