"""
Integration tests for the Sources API.
"""


def test_create_source(test_client):
    resp = test_client.post("/sources/", json={
        "type": "manga_chapter",
        "reference": "Chapter 182",
        "note": "Ichigo's Bankai reveal.",
    })
    assert resp.status_code == 201
    body = resp.json()
    assert body["reference"] == "Chapter 182"
    assert body["type"] == "manga_chapter"


def test_create_source_missing_required_fields_fails(test_client):
    resp = test_client.post("/sources/", json={"note": "Missing type and reference."})
    assert resp.status_code == 422


def test_invalid_source_type_rejected(test_client):
    resp = test_client.post("/sources/", json={"type": "movie", "reference": "Movie 1"})
    assert resp.status_code == 422  # only manga_chapter / anime_episode are valid


def test_get_nonexistent_source_returns_404(test_client):
    resp = test_client.get("/sources/000000000000000000000000")
    assert resp.status_code == 404


def test_list_sources(test_client):
    test_client.post("/sources/", json={"type": "manga_chapter", "reference": "Chapter 1"})
    test_client.post("/sources/", json={"type": "anime_episode", "reference": "Episode 1"})

    resp = test_client.get("/sources/")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_update_source(test_client):
    create_resp = test_client.post("/sources/", json={"type": "manga_chapter", "reference": "Chapter 182"})
    source_id = create_resp.json()["_id"]

    update_resp = test_client.patch(f"/sources/{source_id}", json={"note": "Added context later."})
    assert update_resp.status_code == 200
    assert update_resp.json()["note"] == "Added context later."
    assert update_resp.json()["reference"] == "Chapter 182"  # unchanged


def test_delete_source(test_client):
    create_resp = test_client.post("/sources/", json={"type": "manga_chapter", "reference": "Chapter 182"})
    source_id = create_resp.json()["_id"]

    delete_resp = test_client.delete(f"/sources/{source_id}")
    assert delete_resp.status_code == 204

    get_resp = test_client.get(f"/sources/{source_id}")
    assert get_resp.status_code == 404