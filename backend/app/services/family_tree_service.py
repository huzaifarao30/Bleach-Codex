from typing import List, Dict, Set
from app.repositories.character_repository import CharacterRepository
from app.repositories.relationship_repository import RelationshipRepository
from app.models.relationships import RelationshipType


# Maps each directional type to what it means from the OTHER character's perspective.
# Symmetric types (sibling, spouse, rival, etc.) simply aren't in this map — meaning
# is identical from either side, so no flipping is needed.
DIRECTIONAL_INVERSES: Dict[str, str] = {
    RelationshipType.PARENT: RelationshipType.CHILD,
    RelationshipType.CHILD: RelationshipType.PARENT,
    RelationshipType.CAPTAIN: RelationshipType.LIEUTENANT,
    RelationshipType.LIEUTENANT: RelationshipType.CAPTAIN,
    RelationshipType.SUPERIOR: RelationshipType.SUBORDINATE,
    RelationshipType.SUBORDINATE: RelationshipType.SUPERIOR,
    RelationshipType.MENTOR: RelationshipType.STUDENT,
    RelationshipType.STUDENT: RelationshipType.MENTOR,
    RelationshipType.CREATOR: RelationshipType.CREATED,
    RelationshipType.CREATED: RelationshipType.CREATOR,
}


class FamilyTreeService:
    """
    Builds a graph (nodes + edges) around a starting character by walking the
    relationships collection outward, up to a maximum depth.

    This is where relationship directionality (deferred at the model layer) is
    actually resolved: each edge is labeled with what the relationship means
    FROM THE PERSPECTIVE of the node being expanded, not just stored raw.
    """

    def __init__(self, character_repo: CharacterRepository, relationship_repo: RelationshipRepository):
        self.character_repo = character_repo
        self.relationship_repo = relationship_repo

    def _label_from_perspective(self, relationship_type: str, viewer_is_character_a: bool) -> str:
        """
        Given a raw relationship_type stored as character_a -> character_b,
        return what that relationship means if you're looking FROM character_b's side.
        If viewer_is_character_a, the stored type already reads correctly as-is.
        """
        if viewer_is_character_a:
            return relationship_type
        return DIRECTIONAL_INVERSES.get(relationship_type, relationship_type)

    async def get_family_tree(self, root_character_id: str, max_depth: int = 2) -> dict:
        visited_character_ids: Set[str] = set()
        nodes: List[dict] = []
        edges: List[dict] = []
        seen_edge_ids: Set[str] = set()

        queue: List[tuple] = [(root_character_id, 0)]

        while queue:
            current_id, depth = queue.pop(0)

            if current_id in visited_character_ids:
                continue
            visited_character_ids.add(current_id)

            character = await self.character_repo.get_by_id(current_id)
            if character:
                nodes.append({
                    "id": current_id,
                    "name": character["name"],
                    "portrait_filename": character.get("portrait_filename"),
                })

            if depth >= max_depth:
                continue

            relationships = await self.relationship_repo.list_for_character(current_id)

            for rel in relationships:
                if rel["_id"] in seen_edge_ids:
                    continue
                seen_edge_ids.add(rel["_id"])

                is_a = rel["character_a_id"] == current_id
                other_id = rel["character_b_id"] if is_a else rel["character_a_id"]

                edges.append({
                    "id": rel["_id"],
                    "from_character_id": current_id,
                    "to_character_id": other_id,
                    "relationship_type": self._label_from_perspective(rel["relationship_type"], is_a),
                    "plot_relevance_note": rel.get("plot_relevance_note"),
                })

                if other_id not in visited_character_ids:
                    queue.append((other_id, depth + 1))

        return {"nodes": nodes, "edges": edges}