from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class SourceType(str, Enum):
    """Type of canon source being cited."""

    MANGA_CHAPTER = "manga_chapter"
    ANIME_EPISODE = "anime_episode"


class SourceBase(BaseModel):
    """Shared fields common to every Source variant."""

    type: SourceType = Field(..., description="Whether this source is a manga chapter or anime episode.", examples=["manga_chapter"])
    reference: str = Field(..., description="The specific chapter/episode identifier.", examples=["Chapter 182"])
    note: Optional[str] = Field(None, description="Optional context about what this source covers or is notable for.")


class SourceCreate(SourceBase):
    """Request body for creating a new source."""
    pass


class SourceUpdate(BaseModel):
    """Request body for updating an existing source. Every field optional."""

    type: Optional[SourceType] = Field(None, description="Updated source type.")
    reference: Optional[str] = Field(None, description="Updated chapter/episode reference.")
    note: Optional[str] = Field(None, description="Updated note.")


class SourceResponse(SourceBase):
    """Full source shape returned by the API, including generated id."""

    id: str = Field(..., alias="_id", description="MongoDB-generated unique identifier.")

    class Config:
        populate_by_name = True