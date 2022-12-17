from fastapi import Request
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

card_route = InferringRouter()


@cbv(card_route)
class Card:
    @card_route.get(
        "/test/",
        description="Тестовый API"
    )
    def get_test(self):
        return {"test": "ok"}
