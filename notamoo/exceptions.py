from fastapi import HTTPException


class NoteNotFoundException(HTTPException):
    def __init__(self, slug: str) -> None:
        super().__init__(
            status_code=404, detail=f'Note with slug `{slug}` not found.'
        )


class NoteExpiredException(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=410, detail='Note is expired.')


class NoteViewLimitReachedException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=403, detail='Note has reached its view limit.'
        )


class PasswordMismatchException(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=401, detail='Password does not match.')
