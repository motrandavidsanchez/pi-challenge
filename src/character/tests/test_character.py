from src.settings.conftest import client, cleanup_db_fixture


def test_create_character(client, cleanup_db_fixture):
    data = {
      "name": "Pachito",
      "height": 0,
      "mass": 0,
      "hair_color": "Azul",
      "skin_color": "Amarillo",
      "eye_color": "Marron",
      "birth_year": 0
    }
    response = client.post("/character/add", json=data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Pachito"
    assert data["hair_color"] == "Azul"
    assert data["skin_color"] == "Amarillo"
    assert data["eye_color"] == "Marron"


def test_get_all_character(client, cleanup_db_fixture):
    data = {
      "name": "Pachito",
      "height": 0,
      "mass": 0,
      "hair_color": "Azul",
      "skin_color": "Amarillo",
      "eye_color": "Marron",
      "birth_year": 0
    }
    response = client.post("/character/add", json=data)
    assert response.status_code == 201

    response = client.get("/character/getAll")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1


def test_get_detail_character(client, cleanup_db_fixture):
    data = {
      "name": "Pachito",
      "height": 0,
      "mass": 0,
      "hair_color": "Azul",
      "skin_color": "Amarillo",
      "eye_color": "Marron",
      "birth_year": 0
    }
    response = client.post("/character/add", json=data)
    assert response.status_code == 201
    data_post = response.json()
    id_character = data_post["id"]

    response = client.get(f"/character/get/{id_character}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Pachito"
    assert data["hair_color"] == "Azul"
    assert data["skin_color"] == "Amarillo"
    assert data["eye_color"] == "Marron"


def test_delete_character(client, cleanup_db_fixture):
    data = {
      "name": "Pachito",
      "height": 0,
      "mass": 0,
      "hair_color": "Azul",
      "skin_color": "Amarillo",
      "eye_color": "Marron",
      "birth_year": 0
    }
    response = client.post("/character/add", json=data)
    assert response.status_code == 201
    data_post = response.json()
    id_character = data_post["id"]

    response = client.delete(f"/character/delete/{id_character}")
    assert response.status_code == 200
    data = response.json()
    assert data['detail'] == 'The character has been deleted'
