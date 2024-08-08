from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from notamoo.database import Base, engine
from notamoo.routers import notes


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title='Notamoo',
    summary='Leave special notes for special people!',
    version='v1',
    docs_url='/api/docs/swagger',
    redoc_url='/api/docs/redoc',
    lifespan=lifespan,
)

app.include_router(notes.router, prefix='/api/notes', tags=['Notes'])
