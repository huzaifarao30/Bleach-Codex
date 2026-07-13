from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing import List, Optional
from enum import Enum


class PowerType(str, Enum):
    """Fixed set of power categories, per the design doc's Power System section.

    NOTE: hardcoded for the v1 vertical slice. If category management needs to
    become admin-editable later, this migrates from an Enum to a database-backed
    validated string — a deliberate, deferred decision, not an oversight.
    """

    SHIKAI = "shikai"
    BANKAI = "bankai"
    FULLBRING = "fullbring"
    HOLLOW = "hollow"
    QUINCY = "quincy"
    OTHER = "other"


class PowerBase(BaseModel):
    """Shared fields common to every Power variant."""

    character_id: str = Field(..., description="ID of the character this power belongs to.")
    power_type: PowerType = Field(..., description="Category of power.", examples=["bankai"])
    other_type_label: Optional[str] = Field(
        None, description="Required if power_type is 'other' — describes what the power actually is."
    )
    ability_description: str = Field(..., description="Description of what the power does.")
    rules_and_limitations: Optional[str] = Field(None, description="Canon-stated rules or limitations on this power.")
    evolution_notes: Optional[str] = Field(None, description="How this power changes or upgrades later in the story, if applicable.")
    image_filename: Optional[str] = Field(
        None, description="Image showing this specific form (the weapon, or the character in this "
        "state), stored in frontend assets/powers/. Optional — every form works fine as text-only "
        "until art exists. Never hardcode this filename in frontend code, always read it from here."
    )

    @model_validator(mode="after")
    def require_label_when_other(self):
        if self.power_type == PowerType.OTHER and not self.other_type_label:
            raise ValueError("other_type_label is required when power_type is 'other'.")
        return self


class PowerCreate(PowerBase):
    """Request body for creating a new power. Contradictions linked separately, after creation."""

    first_shown_source_id: Optional[str] = Field(
        None, description="ID of the source where this power is first shown, if known at creation time."
    )


class PowerUpdate(BaseModel):
    """Request body for updating an existing power. Every field optional."""

    power_type: Optional[PowerType] = Field(None, description="Updated power category.")
    other_type_label: Optional[str] = Field(None, description="Updated label if power_type is 'other'.")
    ability_description: Optional[str] = Field(None, description="Updated ability description.")
    rules_and_limitations: Optional[str] = Field(None, description="Updated rules or limitations.")
    evolution_notes: Optional[str] = Field(None, description="Updated evolution notes.")
    first_shown_source_id: Optional[str] = Field(None, description="Updated first-shown source reference.")
    image_filename: Optional[str] = Field(None, description="Updated form image filename.")


class PowerResponse(PowerBase):
    """Full power shape returned by the API, including generated id and linked references."""

    id: str = Field(..., alias="_id", description="MongoDB-generated unique identifier.")
    first_shown_source_id: Optional[str] = Field(None, description="ID of the source where this power is first shown.")
    contradiction_ids: List[str] = Field(default_factory=list, description="IDs of lore_events (contradictions) tied to this power.")

    model_config = ConfigDict(populate_by_name=True)