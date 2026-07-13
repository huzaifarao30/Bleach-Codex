from pydantic import BaseModel, Field
from typing import List, Optional


class CharacterBase(BaseModel):
    """Shared fields common to every Character variant."""

    name: str = Field(..., description="Character's full display name.", examples=["Ichigo Kurosaki"])
    biography: str = Field(..., description="Narrative biography summarizing the character's background.")
    personality: Optional[str] = Field(None, description="Description of the character's personality traits.")
    appearance: Optional[str] = Field(None, description="Physical appearance description.")
    clan_id: Optional[str] = Field(None, description="Reference to the clan/family this character belongs to, if any.")


class CharacterCreate(CharacterBase):
    """Request body for creating a new character. No id or relations yet."""
    pass


class CharacterUpdate(BaseModel):
    """Request body for updating an existing character. Every field optional — only send what's changing."""

    name: Optional[str] = Field(None, description="Updated display name.")
    biography: Optional[str] = Field(None, description="Updated biography.")
    personality: Optional[str] = Field(None, description="Updated personality description.")
    appearance: Optional[str] = Field(None, description="Updated appearance description.")
    clan_id: Optional[str] = Field(None, description="Updated clan/family reference.")


class CharacterResponse(CharacterBase):
    """Full character shape returned by the API, including generated id and linked references."""

    id: str = Field(..., alias="_id", description="MongoDB-generated unique identifier.")
    arc_ids: List[str] = Field(default_factory=list, description="IDs of arcs this character appears in.")
    source_ids: List[str] = Field(default_factory=list, description="IDs of sources backing biographical claims.")

    class Config:
        populate_by_name = True