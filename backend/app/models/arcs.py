from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional


class ArcBase(BaseModel):
    """Shared fields common to every Arc variant."""

    name: str = Field(..., description="Name of the story arc.", examples=["Soul Society Arc"])
    order_index: int = Field(..., description="Sequence position of this arc relative to others, for timeline ordering.")
    chapter_range: Optional[str] = Field(None, description="Manga chapter range covered by this arc.", examples=["Chapters 43–184"])
    episode_range: Optional[str] = Field(None, description="Anime episode range covered by this arc.", examples=["Episodes 20–109"])


class ArcCreate(ArcBase):
    """Request body for creating a new arc. Character list linked separately, after creation."""
    pass


class ArcUpdate(BaseModel):
    """Request body for updating an existing arc. Every field optional."""

    name: Optional[str] = Field(None, description="Updated arc name.")
    order_index: Optional[int] = Field(None, description="Updated sequence position.")
    chapter_range: Optional[str] = Field(None, description="Updated chapter range.")
    episode_range: Optional[str] = Field(None, description="Updated episode range.")


class ArcResponse(ArcBase):
    """Full arc shape returned by the API, including generated id and linked characters."""

    id: str = Field(..., alias="_id", description="MongoDB-generated unique identifier.")
    character_ids: List[str] = Field(default_factory=list, description="IDs of characters who appear in this arc.")

    model_config = ConfigDict(populate_by_name=True)
