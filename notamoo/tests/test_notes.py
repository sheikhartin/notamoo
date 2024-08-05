import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from notamoo import schemas, crud
from notamoo.exceptions import (
    NoteNotFoundException,
    NoteExpiredException,
    NoteViewLimitReachedException,
    PasswordMismatchException,
)


def test_create_note_without_password(db_session_fixture: Session) -> None:
    note_in = schemas.NoteCreate(content='Test note')
    note = crud.create_note(db=db_session_fixture, note=note_in)
    assert note.content == 'Test note'
    assert note.password is None


def test_create_note_with_password(db_session_fixture: Session) -> None:
    note_in = schemas.NoteCreate(content='Test note', password='secret')
    note = crud.create_note(db=db_session_fixture, note=note_in)
    assert note.content == 'Test note'
    assert note.password is not None


def test_read_note_success(db_session_fixture: Session) -> None:
    note_in = schemas.NoteCreate(content='Test note')
    note = crud.create_note(db=db_session_fixture, note=note_in)
    read_note = crud.read_and_update_note_views(
        db=db_session_fixture, slug=note.slug
    )
    assert read_note.content == 'Test note'
    assert read_note.views == 1


@pytest.mark.xfail(raises=NoteNotFoundException)
def test_read_note_not_found(db_session_fixture: Session) -> None:
    crud.read_and_update_note_views(db=db_session_fixture, slug='nonexistent')


@pytest.mark.xfail(raises=NoteExpiredException)
def test_read_note_expired(db_session_fixture: Session) -> None:
    note_in = schemas.NoteCreate(
        content='Test note', expires_at='2000-01-01T00:00:00'
    )
    note = crud.create_note(db=db_session_fixture, note=note_in)
    crud.read_and_update_note_views(db=db_session_fixture, slug=note.slug)


@pytest.mark.xfail(raises=NoteViewLimitReachedException)
def test_read_note_view_limit_reached(db_session_fixture: Session) -> None:
    note_in = schemas.NoteCreate(content='Test note', view_limit=1)
    note = crud.create_note(db=db_session_fixture, note=note_in)
    crud.read_and_update_note_views(db=db_session_fixture, slug=note.slug)
    crud.read_and_update_note_views(db=db_session_fixture, slug=note.slug)


@pytest.mark.xfail(raises=PasswordMismatchException)
def test_read_note_password_mismatch(db_session_fixture: Session) -> None:
    note_in = schemas.NoteCreate(content='Test note', password='secret')
    note = crud.create_note(db=db_session_fixture, note=note_in)
    crud.read_and_update_note_views(
        db=db_session_fixture, slug=note.slug, password='wrongpassword'
    )


def test_create_note_endpoint(test_client_fixture: TestClient) -> None:
    response = test_client_fixture.post(
        '/api/notes/', json={'content': 'Test note'}
    )
    assert response.status_code == 200
    assert response.json()['content'] == 'Test note'


def test_read_note_endpoint(test_client_fixture: TestClient) -> None:
    response = test_client_fixture.post(
        '/api/notes/', json={'content': 'Test note'}
    )
    slug = response.json()['slug']
    response = test_client_fixture.get(f'/api/notes/{slug}')
    assert response.status_code == 200
    assert response.json()['content'] == 'Test note'
    assert response.json()['views'] == 1


def test_read_note_not_found_endpoint(test_client_fixture: TestClient) -> None:
    response = test_client_fixture.get('/api/notes/nonexistent')
    assert response.status_code == 404


def test_read_note_expired_endpoint(test_client_fixture: TestClient) -> None:
    response = test_client_fixture.post(
        '/api/notes/',
        json={'content': 'Test note', 'expires_at': '2000-01-01T00:00:00'},
    )
    slug = response.json()['slug']
    response = test_client_fixture.get(f'/api/notes/{slug}')
    assert response.status_code == 410


def test_read_note_view_limit_reached_endpoint(
    test_client_fixture: TestClient,
) -> None:
    response = test_client_fixture.post(
        '/api/notes/', json={'content': 'Test note', 'view_limit': 1}
    )
    slug = response.json()['slug']
    test_client_fixture.get(f'/api/notes/{slug}')
    response = test_client_fixture.get(f'/api/notes/{slug}')
    assert response.status_code == 403


def test_read_note_password_mismatch_endpoint(
    test_client_fixture: TestClient,
) -> None:
    response = test_client_fixture.post(
        '/api/notes/', json={'content': 'Test note', 'password': 'secret'}
    )
    slug = response.json()['slug']
    response = test_client_fixture.get(
        f'/api/notes/{slug}', params={'password': 'wrongpassword'}
    )
    assert response.status_code == 401
