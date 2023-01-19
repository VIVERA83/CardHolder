from typing import TYPE_CHECKING

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

if TYPE_CHECKING:
    from core.components import Application


async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        content={
            "detail": f"{exc.detail}.",
            "message": f"See the documentation: "
            f"http://{request.app.settings.host}:{request.app.settings.port}{request.app.docs_url}",
        },
        status_code=exc.status_code,
    )


def setup_exception(app: "Application"):
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
