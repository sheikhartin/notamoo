import uuid

from sqlalchemy.orm import Session

from notamoo import schemas, models
from notamoo.utils import get_password_hash


def create_note(db: Session, note: schemas.NoteCreate) -> models.Note:
    db_note = models.Note(
        content=note.content,
        password=get_password_hash(note.password) if note.password else None,
        view_limit=note.view_limit,
        slug=uuid.uuid4().hex[:15],
        expires_at=note.expires_at,
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note
