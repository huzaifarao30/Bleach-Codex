from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class RelationshipType(str, Enum):
    """Relationship types between two characters.

    Directional types (character_a -> character_b carries specific meaning):
    PARENT/CHILD, CAPTAIN/LIEUTENANT, SUPERIOR/SUBORDINATE, MENTOR/STUDENT, CREATOR/CREATED.

    Symmetric types (direction irrelevant): SIBLING, SPOUSE, RIVAL, ENEMY, ALLY, FRIEND.

    NOTE: multiple relationship rows may exist for the same character pair
    (e.g. RIVAL and, separately, ALLY) — no uniqueness constraint on
    (character_a_id, character_b_id) is applied, by design.
    """

    PARENT = "parent"
    CHILD = "child"
    CAPTAIN = "captain"
    LIEUTENANT = "lieutenant"
    SUPERIOR = "superior"
    SUBORDINATE = "subordinate"
    MENTOR = "mentor"
    STUDENT = "student"
    CREATOR = "creator"
    CREATED = "created"
    SIBLING = "sibling"
    SPOUSE = "spouse"
    RIVAL = "rival"
    ENEMY = "enemy"
    ALLY = "ally"
    FRIEND = "friend"


class RelationshipBase(BaseModel):
    """Shared fields common to every Relationship variant."""

    character_a_id: str = Field(..., description="First character in the relationship. For directional types, this is the 'source' side (e.g. the parent, the captain).")
    character_b_id: str = Field(..., description="Second character in the relationship. For directional types, this is the 'target' side (e.g. the child, the lieutenant).")
    relationship_type: RelationshipType = Field(..., description="Type of relationship between the two characters.", examples=["parent"])
    plot_relevance_note: Optional[str] = Field(None, description="Why this connection matters to the story.")


class RelationshipCreate(RelationshipBase):
    """Request body for creating a new relationship edge."""
    pass


class RelationshipUpdate(BaseModel):
    """Request body for updating an existing relationship. Every field optional."""

    relationship_type: Optional[RelationshipType] = Field(None, description="Updated relationship type.")
    plot_relevance_note: Optional[str] = Field(None, description="Updated plot relevance note.")


class RelationshipResponse(RelationshipBase):
    """Full relationship shape returned by the API, including generated id."""

    id: str = Field(..., alias="_id", description="MongoDB-generated unique identifier.")

    class Config:
        populate_by_name = True