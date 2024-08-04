from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict, field_validator


class NoteBase(BaseModel):
    content: str = Field(..., description='The content of the note.')
    password: Optional[str] = Field(
        None, description='Optional password to protect the note.'
    )
    view_limit: Optional[int] = Field(
        None, ge=1, description='Number of times the note can be viewed.'
    )
    expires_at: Optional[str] = Field(
        None,
        description='Expiration date and time for the note in the format `YYYY-MM-DDTHH:MM`.',
    )

    @field_validator('expires_at')
    def validate_expires_at(cls, v: str | None) -> Optional[datetime]:
        return datetime.strptime(v, '%Y-%m-%dT%H:%M') if v is not None else v


class NoteCreate(NoteBase):
    pass


class NoteRead(NoteBase):
    model_config = ConfigDict(from_attributes=True)

    views: int = Field(
        ..., description='Number of times the note has been viewed.'
    )
    slug: str = Field(..., description='Unique slug for the note.')
    created_at: Optional[datetime] = Field(
        None, description='Timestamp when the note was created.'
    )
