from typing import TYPE_CHECKING
from api.v1.card import card_route

if TYPE_CHECKING:
    from core.app import Application


def setup_routes(app: "Application"):
    app.include_router(card_route)
