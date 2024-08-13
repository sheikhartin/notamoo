from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from notamoo import schemas, crud
from notamoo.database import get_db

router = APIRouter()


@router.post('/', response_model=schemas.NoteRead)
async def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    return crud.create_note(db=db, note=note)


@router.get('/{slug}', response_model=schemas.NoteRead)
async def read_note(
    slug: str,
    password: str = Header(None),
    db: Session = Depends(get_db),
):
    return crud.read_and_update_note_views(db=db, slug=slug, password=password)
