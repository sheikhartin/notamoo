import os
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from notamoo.main import app
from notamoo.database import Base, get_db

TEST_DATABASE_NAME = 'test.sqlite3'
TEST_DATABASE_URL = f'sqlite:///./{TEST_DATABASE_NAME}'

engine = create_engine(
    TEST_DATABASE_URL, connect_args={'check_same_thread': False}
)
TestingSessionLocal = sessionmaker(
    bind=engine, autocommit=False, autoflush=False
)

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope='session')
def db_session_fixture() -> Generator[Session, None, None]:
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope='session')
def test_client_fixture(
    db_session_fixture: Session,
) -> Generator[TestClient, None, None]:
    def override_get_db() -> Generator[Session, None, None]:
        try:
            yield db_session_fixture
        finally:
            db_session_fixture.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope='session', autouse=True)
def cleanup_test_database_fixture() -> Generator[None, None, None]:
    yield

    Base.metadata.drop_all(bind=engine)

    if os.path.isfile(TEST_DATABASE_NAME):
        os.remove(TEST_DATABASE_NAME)
        print(
            f'Test database file `{TEST_DATABASE_NAME}` removed successfully.'
        )
    else:
        print(f'Test database file `{TEST_DATABASE_NAME}` does not exist.')
