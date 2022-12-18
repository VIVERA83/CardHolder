from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.helpers import Application


def setup_routes(app: "Application"):
    from card.api.v1.card import card_route
    app.include_router(card_route)
