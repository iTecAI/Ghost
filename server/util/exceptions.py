from starlite import Request, Response
from typing import Optional
import logging

class ApplicationException(Exception):
    def __init__(self, status_code: Optional[int] = 500, error_code: Optional[str] = "error.generic", error_message: Optional[str] = "An unknown error occurred.") -> None:
        super().__init__()
        self.status_code = status_code
        self.error_code = error_code
        self.error_message = error_message
    
    def __repr__(self) -> str:
        return str(self)
    
    def __str__(self) -> str:
        return f"Application Error {self.status_code} : {self.error_code} => {self.error_message}"

def HTTPExceptionHandler(_: Request, exc: Exception) -> Response:
    if exc.status_code == 500:
        logging.exception(str(exc))
    else:
        logging.warning(str(exc))
    status_code = getattr(exc, "status_code", 500)
    detail = getattr(exc, "detail", "")

    return Response(
        content={
            "detail": detail,
            "errorCode": "error.generic"
        },
        status_code=status_code
    )

def ApplicationExceptionHandler(_: Request, exc: ApplicationException) -> Response:
    if exc.status_code == 500:
        logging.exception(str(exc))
    else:
        logging.warning(str(exc))
    return Response(
        content={
            "detail": exc.error_message,
            "errorCode": exc.error_code
        },
        status_code=exc.status_code
    )