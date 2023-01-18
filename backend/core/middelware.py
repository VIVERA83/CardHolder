import logging
import traceback
from typing import TYPE_CHECKING

from fastapi import status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

if TYPE_CHECKING:
    from core.components import Application, Request


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: "Request", call_next):
        try:
            response = await call_next(request)
            response.headers["Custom"] = "Example"
            return response
        except Exception:  # noqa
            logging.error(traceback.format_exc())
            return JSONResponse(
                content={
                    "detail": "Internal error error",
                    "message": "The server is temporarily unavailable try contacting later",
                },
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


def setup_middleware(app: "Application"):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(ErrorHandlingMiddleware)
