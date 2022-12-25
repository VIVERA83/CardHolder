from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.helpers import Application


def setup_routes(app: "Application"):
    from card.views import card_route

    app.include_router(card_route)
