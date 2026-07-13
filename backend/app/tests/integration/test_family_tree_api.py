"""
Integration tests for the Family Tree endpoint — the graph traversal logic.
"""


def _create_character(test_client, name):
    resp = test_client.post("/characters/", json={"name": name, "biography": f"{name}'s biography."})
    return resp.json()["_id"]


def test_family_tree_single_parent_child_edge(test_client):
    isshin_id = _create_character(test_client, "Isshin Kurosaki")
    ichigo_id = _create_character(test_client, "Ichigo Kurosaki")

    test_client.post("/relationships/", json={
        "character_a_id": isshin_id,
        "character_b_id": ichigo_id,
        "relationship_type": "parent",
    })

    resp = test_client.get(f"/family-tree/{ichigo_id}")
    assert resp.status_code == 200
    tree = resp.json()

    node_ids = {n["id"] for n in tree["nodes"]}
    assert isshin_id in node_ids
    assert ichigo_id in node_ids
    assert len(tree["edges"]) == 1


def test_family_tree_directionality_flips_by_perspective(test_client):
    """
    The stored row is Isshin(a) -> parent -> Ichigo(b).
    Expanding FROM Ichigo's side should show it as 'child' (Ichigo is the child),
    not 'parent' -- proving directionality is resolved per-viewer, not just copied raw.
    """
    isshin_id = _create_character(test_client, "Isshin Kurosaki")
    ichigo_id = _create_character(test_client, "Ichigo Kurosaki")

    test_client.post("/relationships/", json={
        "character_a_id": isshin_id,
        "character_b_id": ichigo_id,
        "relationship_type": "parent",
    })

    resp = test_client.get(f"/family-tree/{ichigo_id}")
    tree = resp.json()

    # The edge, when expanded from Ichigo's node, should read as Ichigo -> child -> Isshin
    edge = tree["edges"][0]
    assert edge["from_character_id"] == ichigo_id
    assert edge["to_character_id"] == isshin_id
    assert edge["relationship_type"] == "child"


def test_family_tree_symmetric_type_does_not_flip(test_client):
    byakuya_id = _create_character(test_client, "Byakuya Kuchiki")
    ichigo_id = _create_character(test_client, "Ichigo Kurosaki")

    test_client.post("/relationships/", json={
        "character_a_id": byakuya_id,
        "character_b_id": ichigo_id,
        "relationship_type": "rival",
    })

    resp = test_client.get(f"/family-tree/{ichigo_id}")
    tree = resp.json()

    edge = tree["edges"][0]
    assert edge["relationship_type"] == "rival"  # unchanged regardless of perspective


def test_family_tree_depth_limits_traversal(test_client):
    """Isshin -> Ichigo -> Karin, a 3-character chain. depth=1 from Ichigo should only reach 2 characters."""
    isshin_id = _create_character(test_client, "Isshin Kurosaki")
    ichigo_id = _create_character(test_client, "Ichigo Kurosaki")
    karin_id = _create_character(test_client, "Karin Kurosaki")

    test_client.post("/relationships/", json={
        "character_a_id": isshin_id, "character_b_id": ichigo_id, "relationship_type": "parent",
    })
    test_client.post("/relationships/", json={
        "character_a_id": ichigo_id, "character_b_id": karin_id, "relationship_type": "sibling",
    })

    resp_depth1 = test_client.get(f"/family-tree/{isshin_id}", params={"depth": 1})
    node_ids_depth1 = {n["id"] for n in resp_depth1.json()["nodes"]}
    assert karin_id not in node_ids_depth1  # 2 hops away, shouldn't appear at depth=1

    resp_depth2 = test_client.get(f"/family-tree/{isshin_id}", params={"depth": 2})
    node_ids_depth2 = {n["id"] for n in resp_depth2.json()["nodes"]}
    assert karin_id in node_ids_depth2  # now reachable


def test_family_tree_no_relationships_returns_single_node(test_client):
    lonely_id = _create_character(test_client, "Unconnected Character")

    resp = test_client.get(f"/family-tree/{lonely_id}")
    tree = resp.json()
    assert len(tree["nodes"]) == 1
    assert len(tree["edges"]) == 0