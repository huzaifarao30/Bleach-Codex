"""
Integration tests for GET /characters/{id}/full — the composed character page endpoint.
"""


def _create_character(test_client, name, **extra):
    payload = {"name": name, "biography": f"{name}'s biography."}
    payload.update(extra)
    resp = test_client.post("/characters/", json=payload)
    return resp.json()["_id"]


def test_full_profile_includes_powers(test_client):
    ichigo_id = _create_character(test_client, "Ichigo Kurosaki")
    test_client.post("/powers/", json={
        "character_id": ichigo_id, "power_type": "bankai", "ability_description": "Tensa Zangetsu.",
    })

    resp = test_client.get(f"/characters/{ichigo_id}/full")
    assert resp.status_code == 200
    body = resp.json()
    assert len(body["powers"]) == 1
    assert body["powers"][0]["power_type"] == "bankai"


def test_full_profile_relationship_direction_resolved_correctly(test_client):
    """
    Stored row: Isshin(a) --parent--> Ichigo(b).
    On ICHIGO's full profile, this must read as 'child', not raw 'parent'.
    """
    isshin_id = _create_character(test_client, "Isshin Kurosaki")
    ichigo_id = _create_character(test_client, "Ichigo Kurosaki")

    test_client.post("/relationships/", json={
        "character_a_id": isshin_id, "character_b_id": ichigo_id, "relationship_type": "parent",
    })

    resp = test_client.get(f"/characters/{ichigo_id}/full")
    body = resp.json()
    assert len(body["relationships"]) == 1
    rel = body["relationships"][0]
    assert rel["relationship_type"] == "child"
    assert rel["other_character_name"] == "Isshin Kurosaki"

    # And from Isshin's side, it should read as 'parent', unchanged.
    isshin_resp = test_client.get(f"/characters/{isshin_id}/full")
    isshin_rel = isshin_resp.json()["relationships"][0]
    assert isshin_rel["relationship_type"] == "parent"
    assert isshin_rel["other_character_name"] == "Ichigo Kurosaki"


def test_full_profile_includes_arcs_field(test_client):
    """
    Note: there's no endpoint yet to LINK an arc to a character (arc_ids stays
    empty on creation) — this just confirms the 'arcs' field exists and is
    correctly empty until that linking feature is built.
    """
    character_id = _create_character(test_client, "Ichigo Kurosaki")
    resp = test_client.get(f"/characters/{character_id}/full")
    body = resp.json()
    assert "arcs" in body
    assert body["arcs"] == []


def test_full_profile_nonexistent_character_returns_404(test_client):
    resp = test_client.get("/characters/000000000000000000000000/full")
    assert resp.status_code == 404


def test_full_profile_character_with_nothing_linked(test_client):
    lonely_id = _create_character(test_client, "Unconnected Character")
    resp = test_client.get(f"/characters/{lonely_id}/full")
    body = resp.json()
    assert body["powers"] == []
    assert body["relationships"] == []
    assert body["arcs"] == []