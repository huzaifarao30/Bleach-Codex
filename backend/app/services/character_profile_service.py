import asyncio
from typing import Optional
from app.repositories.character_repository import CharacterRepository
from app.repositories.power_repository import PowerRepository
from app.repositories.relationship_repository import RelationshipRepository
from app.repositories.arc_repository import ArcRepository
from app.services.family_tree_service import DIRECTIONAL_INVERSES


class CharacterProfileService:
    """
    Composes a full character page: bio + powers + relationships (with the
    connected character's name resolved, not just their id) + arcs.

    Like FamilyTreeService, this doesn't own a collection — it's a computed
    view built by combining several existing repositories. Reuses the same
    directionality-flip logic as FamilyTreeService so relationship types read
    correctly from THIS character's perspective, not raw as stored.

    Performance note: every lookup that doesn't depend on another lookup's
    result runs concurrently via asyncio.gather, not sequentially. Against a
    remote database (Atlas), each round-trip has real network latency —
    doing them one-at-a-time in a loop turns N relationships into N separate
    waits stacked end to end. Gathering them runs all N at once instead.
    """

    def __init__(
        self,
        character_repo: CharacterRepository,
        power_repo: PowerRepository,
        relationship_repo: RelationshipRepository,
        arc_repo: ArcRepository,
    ):
        self.character_repo = character_repo
        self.power_repo = power_repo
        self.relationship_repo = relationship_repo
        self.arc_repo = arc_repo

    async def get_full_profile(self, character_id: str) -> Optional[dict]:
        character = await self.character_repo.get_by_id(character_id)
        if not character:
            return None

        # Powers and relationships don't depend on each other — fetch both at once.
        powers, raw_relationships = await asyncio.gather(
            self.power_repo.list_for_character(character_id),
            self.relationship_repo.list_for_character(character_id),
        )

        # Every relationship's "other character" lookup is independent of the
        # others — fetch all of them concurrently instead of one at a time.
        other_ids = [
            rel["character_b_id"] if rel["character_a_id"] == character_id else rel["character_a_id"]
            for rel in raw_relationships
        ]
        other_characters = await asyncio.gather(
            *(self.character_repo.get_by_id(oid) for oid in other_ids)
        )

        relationships = []
        for rel, other_id, other_character in zip(raw_relationships, other_ids, other_characters):
            is_a = rel["character_a_id"] == character_id
            raw_type = rel["relationship_type"]
            resolved_type = raw_type if is_a else DIRECTIONAL_INVERSES.get(raw_type, raw_type)

            relationships.append({
                "id": rel["_id"],
                "other_character_id": other_id,
                "other_character_name": other_character["name"] if other_character else "Unknown",
                "relationship_type": resolved_type,
                "plot_relevance_note": rel.get("plot_relevance_note"),
            })

        # Same idea for arcs — fetch them all concurrently.
        arc_docs = await asyncio.gather(
            *(self.arc_repo.get_by_id(aid) for aid in character.get("arc_ids", []))
        )
        arcs = [{"id": a["_id"], "name": a["name"]} for a in arc_docs if a]

        return {
            "id": character["_id"],
            "name": character["name"],
            "biography": character["biography"],
            "personality": character.get("personality"),
            "appearance": character.get("appearance"),
            "portrait_filename": character.get("portrait_filename"),
            "full_body_filename": character.get("full_body_filename"),
            "powers": powers,
            "relationships": relationships,
            "arcs": arcs,
        }