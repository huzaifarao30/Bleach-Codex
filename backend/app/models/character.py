from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional


class CharacterBase(BaseModel):
    """Shared fields common to every Character variant."""

    name: str = Field(..., description="Character's full display name.", examples=["Ichigo Kurosaki"])
    biography: str = Field(..., description="Narrative biography summarizing the character's background.")
    personality: Optional[str] = Field(None, description="Description of the character's personality traits.")
    appearance: Optional[str] = Field(None, description="Physical appearance description.")
    clan_id: Optional[str] = Field(None, description="Reference to the clan/family this character belongs to, if any.")
    portrait_filename: Optional[str] = Field(None, description="Face/headshot image filename, used on the character card. Stored in frontend assets/characters/ — never hardcoded in frontend code.")
    full_body_filename: Optional[str] = Field(None, description="Full-body image filename, used on the character detail page. Stored in frontend assets/characters/ — never hardcoded in frontend code.")


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
    portrait_filename: Optional[str] = Field(None, description="Updated portrait (card) filename.")
    full_body_filename: Optional[str] = Field(None, description="Updated full-body (detail page) filename.")


class CharacterResponse(CharacterBase):
    """Full character shape returned by the API, including generated id and linked references."""

    id: str = Field(..., alias="_id", description="MongoDB-generated unique identifier.")
    arc_ids: List[str] = Field(default_factory=list, description="IDs of arcs this character appears in.")
    source_ids: List[str] = Field(default_factory=list, description="IDs of sources backing biographical claims.")

    model_config = ConfigDict(populate_by_name=True)