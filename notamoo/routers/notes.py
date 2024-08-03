from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from notamoo import schemas, crud
from notamoo.database import get_db

router = APIRouter(prefix='/notes')


@router.post('/', response_model=schemas.NoteRead)
async def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    return crud.create_note(db=db, note=note)
