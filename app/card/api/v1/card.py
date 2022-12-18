from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from app.core.helpers import Request
from card.models import DurationEnum
from icecream import ic

card_route = InferringRouter()


@cbv(card_route)
class Card:
    @card_route.get(
        "/test/",
        description="Тестовый API"
    )
    async def get_test(self, request: "Request"):
        ic(request.app.settings)
        ic(await request.app.store.card.create_cards(1, 2, DurationEnum.month))
        return {"test": "ok"}
