from fastapi import FastAPI

from notamoo.database import Base, engine
from notamoo.routers import notes

app = FastAPI(
    title='Notamoo',
    summary='Leave special notes for special people!',
    version='v1',
    docs_url='/docs/swagger',
    redoc_url='/docs/redoc',
)

app.include_router(notes.router)


@app.on_event('startup')
async def startup_event() -> None:
    Base.metadata.create_all(engine)
