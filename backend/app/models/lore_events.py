from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing import List, Optional
from enum import Enum


class LoreEventType(str, Enum):
    """What kind of lore event this record represents."""

    FORESHADOWING_HINT = "foreshadowing_hint"
    PAYOFF = "payoff"
    CONTRADICTION = "contradiction"


class LoreEventStatus(str, Enum):
    """Review status — mainly relevant for contradiction entries, per the Plot Hole Tracker's review workflow."""

    PROPOSED = "proposed"
    APPROVED = "approved"
    REJECTED = "rejected"


class LoreEventBase(BaseModel):
    """Shared fields common to every LoreEvent variant."""

    event_type: LoreEventType = Field(..., description="Type of lore event.", examples=["foreshadowing_hint"])
    linked_event_id: Optional[str] = Field(
        None,
        description="For foreshadowing_hint/payoff, the id of the corresponding hint/payoff. Null for contradictions.",
    )
    character_ids: List[str] = Field(default_factory=list, description="IDs of characters involved in this event.")
    description: str = Field(..., description="Explanation of the hint, payoff, or contradiction.")
    status: LoreEventStatus = Field(
        default=LoreEventStatus.APPROVED,
        description="Review status. Defaults to 'approved' for manually-entered entries; set to 'proposed' for AI-suggested candidates awaiting review.",
    )
    source_ids: List[str] = Field(default_factory=list, description="IDs of sources backing this entry. Required — every claim must be citable.")

    @model_validator(mode="after")
    def require_linked_event_for_foreshadowing(self):
        if self.event_type in (LoreEventType.FORESHADOWING_HINT, LoreEventType.PAYOFF) and not self.linked_event_id:
            raise ValueError("linked_event_id is required for foreshadowing_hint and payoff events.")
        return self

    @model_validator(mode="after")
    def require_at_least_one_source(self):
        if not self.source_ids:
            raise ValueError("At least one source_id is required — lore events must be citable.")
        return self


class LoreEventCreate(LoreEventBase):
    """Request body for creating a new lore event."""
    pass


class LoreEventUpdate(BaseModel):
    """Request body for updating an existing lore event. Every field optional."""

    linked_event_id: Optional[str] = Field(None, description="Updated linked event reference.")
    character_ids: Optional[List[str]] = Field(None, description="Updated character list.")
    description: Optional[str] = Field(None, description="Updated description.")
    status: Optional[LoreEventStatus] = Field(None, description="Updated review status.")
    source_ids: Optional[List[str]] = Field(None, description="Updated source list.")


class LoreEventResponse(LoreEventBase):
    """Full lore event shape returned by the API, including generated id.

    `sources` holds the fully resolved source details (joined in by the service
    layer) so the frontend never has to make a second request just to display
    a citation — see the Source<->LoreEvent join discussion in the schema design.
    """

    id: str = Field(..., alias="_id", description="MongoDB-generated unique identifier.")
    sources: List[dict] = Field(default_factory=list, description="Fully resolved source details for source_ids, joined in by the service layer.")

    model_config = ConfigDict(populate_by_name=True)