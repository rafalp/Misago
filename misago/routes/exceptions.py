from starlette.exceptions import HTTPException


class HTTPNotFound(HTTPException):
    def __init__(self, detail: str = None):
        super().__init__(404, detail)
