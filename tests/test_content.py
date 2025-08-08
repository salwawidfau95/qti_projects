import pytest

def test_user_create_content(client, user_token_headers):
    payload = {
        "title": "Judul Konten User",
        "body": "Isi konten milik user"
    }
    response = client.post("/content/", headers=user_token_headers, json=payload)
    assert response.status_code == 200
    assert response.json()["content"]["title"] == "Judul Konten User"
    
    # Simpan ID konten untuk test lain
    global created_content_id
    created_content_id = response.json()["content"]["id"]

def test_user_get_own_content(client, user_token_headers):
    response = client.get("/content/", headers=user_token_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(content["id"] == created_content_id for content in response.json())

def test_user_get_own_content_by_id(client, user_token_headers):
    response = client.get(f"/content/{created_content_id}", headers=user_token_headers)
    assert response.status_code == 200
    assert response.json()["id"] == created_content_id

def test_user_update_own_content(client, user_token_headers):
    payload = {
        "title": "Konten Sudah Diubah",
        "body": "Isi baru setelah diedit"
    }
    response = client.put(f"/content/{created_content_id}", headers=user_token_headers, json=payload)
    assert response.status_code == 200
    assert response.json()["content"]["title"] == "Konten Sudah Diubah"

def test_user_delete_own_content(client, user_token_headers):
    response = client.delete(f"/content/{created_content_id}", headers=user_token_headers)
    assert response.status_code == 200

    # Pastikan sudah tidak bisa diakses
    check = client.get(f"/content/{created_content_id}", headers=user_token_headers)
    assert check.status_code in [403, 404]
