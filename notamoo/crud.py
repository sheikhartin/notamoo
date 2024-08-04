import uuid
from typing import Optional

from sqlalchemy.orm import Session

from notamoo import schemas, models
from notamoo.utils import get_password_hash, verify_password
from notamoo.exceptions import (
    NoteNotFoundException,
    NoteExpiredException,
    NoteViewLimitReachedException,
    PasswordMismatchException,
)


def _create_note_slug(db: Session) -> str:
    while True:
        slug = uuid.uuid4().hex[:15]
        if (
            db.query(models.Note).filter(models.Note.slug == slug).first()
        ) is None:
            return slug


def create_note(db: Session, note: schemas.NoteCreate) -> models.Note:
    db_note = models.Note(
        content=note.content,
        password=(
            get_password_hash(note.password)
            if note.password is not None
            else None
        ),
        view_limit=note.view_limit,
        slug=_create_note_slug(db),
        expires_at=note.expires_at,
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def read_and_update_note_views(
    db: Session,
    slug: str,
    password: Optional[str] = None,
) -> models.Note:
    db_note = db.query(models.Note).filter(models.Note.slug == slug).first()
    if db_note is None:
        raise NoteNotFoundException(slug)
    elif db_note.is_expired():
        raise NoteExpiredException()
    elif db_note.has_reached_view_limit():
        raise NoteViewLimitReachedException()
    elif db_note.password is not None and (
        password is None or not verify_password(password, db_note.password)
    ):
        raise PasswordMismatchException()
    db_note.views += 1
    db.commit()
    db.refresh(db_note)
    return db_note
