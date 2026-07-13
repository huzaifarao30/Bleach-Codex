"""
Integration tests for the Character API — covers the full router -> service -> repository ->
model path, using an in-memory mock database (see conftest.py's test_client fixture).
"""


def test_health_check(test_client):
    resp = test_client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_create_character(test_client):
    resp = test_client.post("/characters/", json={
        "name": "Ichigo Kurosaki",
        "biography": "A substitute Shinigami who protects his hometown of Karakura Town.",
        "personality": "Brash but deeply protective of his friends and family.",
    })
    assert resp.status_code == 201
    body = resp.json()
    assert body["name"] == "Ichigo Kurosaki"
    assert body["arc_ids"] == []
    assert body["source_ids"] == []
    assert "_id" in body


def test_create_character_missing_required_field_fails(test_client):
    resp = test_client.post("/characters/", json={"name": "No Bio Character"})
    assert resp.status_code == 422


def test_get_character_by_id(test_client):
    create_resp = test_client.post("/characters/", json={
        "name": "Rukia Kuchiki",
        "biography": "A Shinigami of the Kuchiki noble family.",
    })
    character_id = create_resp.json()["_id"]

    resp = test_client.get(f"/characters/{character_id}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Rukia Kuchiki"


def test_get_nonexistent_character_returns_404(test_client):
    resp = test_client.get("/characters/000000000000000000000000")
    assert resp.status_code == 404


def test_list_characters(test_client):
    test_client.post("/characters/", json={"name": "Character A", "biography": "Bio A."})
    test_client.post("/characters/", json={"name": "Character B", "biography": "Bio B."})

    resp = test_client.get("/characters/")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_partial_update_only_changes_specified_field(test_client):
    create_resp = test_client.post("/characters/", json={
        "name": "Ichigo Kurosaki",
        "biography": "Original bio.",
    })
    character_id = create_resp.json()["_id"]

    resp = test_client.patch(f"/characters/{character_id}", json={"biography": "Updated bio."})
    assert resp.status_code == 200
    body = resp.json()
    assert body["biography"] == "Updated bio."
    assert body["name"] == "Ichigo Kurosaki"  # unchanged


def test_delete_character(test_client):
    create_resp = test_client.post("/characters/", json={
        "name": "Temporary Character",
        "biography": "Will be deleted.",
    })
    character_id = create_resp.json()["_id"]

    delete_resp = test_client.delete(f"/characters/{character_id}")
    assert delete_resp.status_code == 204

    get_resp = test_client.get(f"/characters/{character_id}")
    assert get_resp.status_code == 404


def test_delete_nonexistent_character_returns_404(test_client):
    resp = test_client.delete("/characters/000000000000000000000000")
    assert resp.status_code == 404
