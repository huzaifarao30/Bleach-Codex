"""
Integration tests for the Powers API.
"""


def _create_character(test_client, name):
    resp = test_client.post("/characters/", json={"name": name, "biography": f"{name}'s biography."})
    return resp.json()["_id"]


def test_create_power(test_client):
    ichigo_id = _create_character(test_client, "Ichigo Kurosaki")

    resp = test_client.post("/powers/", json={
        "character_id": ichigo_id,
        "power_type": "bankai",
        "ability_description": "Tensa Zangetsu grants increased speed and a black blade.",
    })
    assert resp.status_code == 201
    body = resp.json()
    assert body["power_type"] == "bankai"
    assert body["contradiction_ids"] == []


def test_create_power_other_type_requires_label(test_client):
    ichigo_id = _create_character(test_client, "Ichigo Kurosaki")

    resp = test_client.post("/powers/", json={
        "character_id": ichigo_id,
        "power_type": "other",
        "ability_description": "Some unique ability not covered by the standard categories.",
    })
    assert resp.status_code == 422  # rejected — other_type_label missing


def test_create_power_other_type_with_label_succeeds(test_client):
    ichigo_id = _create_character(test_client, "Ichigo Kurosaki")

    resp = test_client.post("/powers/", json={
        "character_id": ichigo_id,
        "power_type": "other",
        "other_type_label": "Final Getsuga Tensho",
        "ability_description": "A forbidden technique that permanently costs the user their powers.",
    })
    assert resp.status_code == 201
    assert resp.json()["other_type_label"] == "Final Getsuga Tensho"


def test_list_powers_for_character(test_client):
    ichigo_id = _create_character(test_client, "Ichigo Kurosaki")
    rukia_id = _create_character(test_client, "Rukia Kuchiki")

    test_client.post("/powers/", json={
        "character_id": ichigo_id, "power_type": "bankai", "ability_description": "Tensa Zangetsu.",
    })
    test_client.post("/powers/", json={
        "character_id": rukia_id, "power_type": "shikai", "ability_description": "Sode no Shirayuki.",
    })

    resp = test_client.get(f"/powers/character/{ichigo_id}")
    assert resp.status_code == 200
    assert len(resp.json()) == 1
    assert resp.json()[0]["power_type"] == "bankai"


def test_get_nonexistent_power_returns_404(test_client):
    resp = test_client.get("/powers/000000000000000000000000")
    assert resp.status_code == 404


def test_invalid_power_type_rejected(test_client):
    ichigo_id = _create_character(test_client, "Ichigo Kurosaki")
    resp = test_client.post("/powers/", json={
        "character_id": ichigo_id,
        "power_type": "not_a_real_type",
        "ability_description": "x",
    })
    assert resp.status_code == 422


def test_update_power(test_client):
    ichigo_id = _create_character(test_client, "Ichigo Kurosaki")
    create_resp = test_client.post("/powers/", json={
        "character_id": ichigo_id, "power_type": "bankai", "ability_description": "Original description.",
    })
    power_id = create_resp.json()["_id"]

    update_resp = test_client.patch(f"/powers/{power_id}", json={"ability_description": "Updated description."})
    assert update_resp.status_code == 200
    assert update_resp.json()["ability_description"] == "Updated description."


def test_delete_power(test_client):
    ichigo_id = _create_character(test_client, "Ichigo Kurosaki")
    create_resp = test_client.post("/powers/", json={
        "character_id": ichigo_id, "power_type": "bankai", "ability_description": "x",
    })
    power_id = create_resp.json()["_id"]

    delete_resp = test_client.delete(f"/powers/{power_id}")
    assert delete_resp.status_code == 204

    get_resp = test_client.get(f"/powers/{power_id}")
    assert get_resp.status_code == 404