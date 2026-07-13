"""
Integration tests for the Relationships API.
"""


def _create_character(test_client, name):
    resp = test_client.post("/characters/", json={"name": name, "biography": f"{name}'s biography."})
    return resp.json()["_id"]


def test_create_relationship(test_client):
    isshin_id = _create_character(test_client, "Isshin Kurosaki")
    ichigo_id = _create_character(test_client, "Ichigo Kurosaki")

    resp = test_client.post("/relationships/", json={
        "character_a_id": isshin_id,
        "character_b_id": ichigo_id,
        "relationship_type": "parent",
        "plot_relevance_note": "Isshin is Ichigo's father and a former Shinigami captain.",
    })
    assert resp.status_code == 201
    body = resp.json()
    assert body["relationship_type"] == "parent"
    assert body["character_a_id"] == isshin_id
    assert body["character_b_id"] == ichigo_id


def test_multiple_relationship_types_between_same_pair(test_client):
    """Confirms the edge-list design allows two relationship rows for the same character pair."""
    byakuya_id = _create_character(test_client, "Byakuya Kuchiki")
    ichigo_id = _create_character(test_client, "Ichigo Kurosaki")

    resp1 = test_client.post("/relationships/", json={
        "character_a_id": byakuya_id,
        "character_b_id": ichigo_id,
        "relationship_type": "rival",
    })
    resp2 = test_client.post("/relationships/", json={
        "character_a_id": byakuya_id,
        "character_b_id": ichigo_id,
        "relationship_type": "ally",
    })
    assert resp1.status_code == 201
    assert resp2.status_code == 201

    all_resp = test_client.get("/relationships/")
    assert len(all_resp.json()) == 2


def test_list_relationships_for_character_finds_both_sides(test_client):
    """A character should show up whether they're character_a or character_b in the row."""
    isshin_id = _create_character(test_client, "Isshin Kurosaki")
    ichigo_id = _create_character(test_client, "Ichigo Kurosaki")
    masaki_id = _create_character(test_client, "Masaki Kurosaki")

    test_client.post("/relationships/", json={
        "character_a_id": isshin_id, "character_b_id": ichigo_id, "relationship_type": "parent",
    })
    test_client.post("/relationships/", json={
        "character_a_id": ichigo_id, "character_b_id": masaki_id, "relationship_type": "child",
    })

    resp = test_client.get(f"/relationships/character/{ichigo_id}")
    assert resp.status_code == 200
    results = resp.json()
    assert len(results) == 2  # Ichigo appears as character_b in one row, character_a in the other


def test_get_nonexistent_relationship_returns_404(test_client):
    resp = test_client.get("/relationships/000000000000000000000000")
    assert resp.status_code == 404


def test_invalid_relationship_type_rejected(test_client):
    a_id = _create_character(test_client, "Character A")
    b_id = _create_character(test_client, "Character B")

    resp = test_client.post("/relationships/", json={
        "character_a_id": a_id,
        "character_b_id": b_id,
        "relationship_type": "not_a_real_type",
    })
    assert resp.status_code == 422


def test_update_relationship_type(test_client):
    a_id = _create_character(test_client, "Character A")
    b_id = _create_character(test_client, "Character B")

    create_resp = test_client.post("/relationships/", json={
        "character_a_id": a_id, "character_b_id": b_id, "relationship_type": "rival",
    })
    relationship_id = create_resp.json()["_id"]

    update_resp = test_client.patch(f"/relationships/{relationship_id}", json={"relationship_type": "ally"})
    assert update_resp.status_code == 200
    assert update_resp.json()["relationship_type"] == "ally"


def test_delete_relationship(test_client):
    a_id = _create_character(test_client, "Character A")
    b_id = _create_character(test_client, "Character B")

    create_resp = test_client.post("/relationships/", json={
        "character_a_id": a_id, "character_b_id": b_id, "relationship_type": "friend",
    })
    relationship_id = create_resp.json()["_id"]

    delete_resp = test_client.delete(f"/relationships/{relationship_id}")
    assert delete_resp.status_code == 204

    get_resp = test_client.get(f"/relationships/{relationship_id}")
    assert get_resp.status_code == 404