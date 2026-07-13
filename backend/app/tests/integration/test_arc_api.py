"""
Integration tests for the Arcs API.
"""


def test_create_arc(test_client):
    resp = test_client.post("/arcs/", json={
        "name": "Soul Society Arc",
        "order_index": 1,
        "chapter_range": "Chapters 43-184",
        "episode_range": "Episodes 20-109",
    })
    assert resp.status_code == 201
    body = resp.json()
    assert body["name"] == "Soul Society Arc"
    assert body["character_ids"] == []


def test_create_arc_missing_order_index_fails(test_client):
    resp = test_client.post("/arcs/", json={"name": "Some Arc"})
    assert resp.status_code == 422  # order_index is required


def test_list_arcs_sorted_by_order_index(test_client):
    """Arcs should always come back in timeline order, regardless of creation order."""
    test_client.post("/arcs/", json={"name": "Arrancar Arc", "order_index": 2})
    test_client.post("/arcs/", json={"name": "Soul Society Arc", "order_index": 1})
    test_client.post("/arcs/", json={"name": "Thousand-Year Blood War Arc", "order_index": 3})

    resp = test_client.get("/arcs/")
    assert resp.status_code == 200
    names_in_order = [arc["name"] for arc in resp.json()]
    assert names_in_order == ["Soul Society Arc", "Arrancar Arc", "Thousand-Year Blood War Arc"]


def test_get_nonexistent_arc_returns_404(test_client):
    resp = test_client.get("/arcs/000000000000000000000000")
    assert resp.status_code == 404


def test_update_arc(test_client):
    create_resp = test_client.post("/arcs/", json={"name": "Soul Society Arc", "order_index": 1})
    arc_id = create_resp.json()["_id"]

    update_resp = test_client.patch(f"/arcs/{arc_id}", json={"chapter_range": "Chapters 43-184"})
    assert update_resp.status_code == 200
    assert update_resp.json()["chapter_range"] == "Chapters 43-184"
    assert update_resp.json()["name"] == "Soul Society Arc"  # unchanged


def test_delete_arc(test_client):
    create_resp = test_client.post("/arcs/", json={"name": "Soul Society Arc", "order_index": 1})
    arc_id = create_resp.json()["_id"]

    delete_resp = test_client.delete(f"/arcs/{arc_id}")
    assert delete_resp.status_code == 204

    get_resp = test_client.get(f"/arcs/{arc_id}")
    assert get_resp.status_code == 404