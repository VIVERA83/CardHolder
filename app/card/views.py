from typing import Optional
from uuid import UUID

from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from card.models import StatusCardEnum
from card.schemes import (
    CardSchema,
    CardShortSchema,
    CardTransactionsSchema,
    CreateCardSchema,
    SearchSchema,
)
from core.helpers import Request

card_route = InferringRouter()


@cbv(card_route)
class Card:
    @card_route.post(
        "/create_cards/",
        summary="Генерация карт",
        description="Генерация карт, в соответствии с указанной серией - `series` и  количеством - `count`",
        response_description="Список карт",
    )
    async def create_cards(
        self,
        request: "Request",
        data: CreateCardSchema,
    ) -> list[CardShortSchema]:
        return await request.app.store.card.create_cards(
            series=data.series, count=data.count, duration=data.duration.modified()
        )

    @card_route.post(
        "/search/",
        summary="Поиск карт",
        description="Поиск карты по параметрам",
        response_description="Список карт",
    )
    async def search(
        self, request: "Request", search_params: SearchSchema
    ) -> list[CardShortSchema]:
        return await request.app.store.card.get_cards(
            series=search_params.series,
            number=search_params.number,
            create_data=search_params.create_data,
            expire_date=search_params.expire_date,
            status=search_params.status,
            page_number=search_params.page_number,
            page_size=search_params.page_size,
        )

    @card_route.get(
        "/get_card/",
        summary="Данные по карте",
        description="Профиль карты, с историей операций",
        response_description="Детальная информация по карте",
    )
    async def get_card(
        self, request: "Request", series: int, number: int
    ) -> Optional[CardSchema]:
        return await request.app.store.card.get_card(series=series, number=number)

    @card_route.post(
        "/create_transaction/",
        summary="Создать операцию по карте",
        description="Провести операцию по карте",
        response_description="Детальная информация по проведенной операции",
    )
    async def create_transaction(
        self, request: "Request", id_card: UUID, amount: float
    ) -> Optional[CardTransactionsSchema]:
        return await request.app.store.card.create_transaction(
            id_card=id_card, amount=amount
        )

    @card_route.put(
        "/update_card_status/",
        summary="Обновление статуса карты",
        description="Изменение статуса карты",
        response_description="Детальная информация по обновленной карте",
    )
    async def update_card_status(
        self, request: "Request", id_card: UUID, status: StatusCardEnum
    ) -> Optional[CardShortSchema]:
        return await request.app.store.card.update_card_status(
            id_card=id_card, status=status
        )

    @card_route.delete(
        "/delete_card/",
        summary="Удалить карту",
        description="Удаление карты и истории операций по карте",
        response_description="Детальная информация по удаленной карте",
    )
    async def delete_card(
        self, request: "Request", id_card: UUID
    ) -> Optional[CardSchema]:
        return await request.app.store.card.delete_card(id_card=id_card)
