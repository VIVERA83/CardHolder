from datetime import date
from typing import Optional
from uuid import UUID

from card.models import StatusCardEnum
from card.query_params import (
    query_create_date,
    query_expire_date,
    query_id,
    query_number,
    query_page_number,
    query_page_size,
    query_series,
    query_status,
)
from card.schemes import (
    CardSchema,
    CardTransactionsSchema,
    CreateCardSchema,
    DurationEnumStr,
)
from card.utils import get_annotations_to_str
from core.components import Request
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

card_route = InferringRouter()


@cbv(card_route)
class Card:
    @card_route.post(
        "/create_cards/",
        summary="Генерация карт",
        description=f"Генерация карт, в соответствии с указанной серией - `series` и  количеством "
        f"- `count`\n сроком действия - `duration` : {get_annotations_to_str(DurationEnumStr)}",
        response_description="Список карт",
        tags=["POST"],
    )
    async def create_cards(
        self,
        request: "Request",
        data: CreateCardSchema,
    ) -> list[CardSchema]:
        return await request.app.store.card.create_cards(
            series=data.series, count=data.count, duration=data.duration.modified()
        )

    @card_route.post(
        "/create_transaction/",
        summary="Создать операцию по карте",
        description="Провести операцию по карте",
        response_description="Детальная информация по проведенной операции",
        tags=["POST"],
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
        tags=["PUT"],
    )
    async def update_card_status(
        self, request: "Request", id_card: UUID, status: StatusCardEnum
    ) -> Optional[CardSchema]:
        return await request.app.store.card.update_card_status(
            id_card=id_card, status=status
        )

    @card_route.delete(
        "/delete_card/",
        summary="Удалить карту",
        description="Удаление карты и истории операций по карте",
        response_description="Детальная информация по удаленной карте",
        tags=["DELETE"],
    )
    async def delete_card(
        self, request: "Request", id_card: UUID
    ) -> Optional[CardSchema]:
        return await request.app.store.card.delete_card(id_card=id_card)

    @card_route.get(
        "/get_card/",
        summary="Данные по карте",
        description="Профиль карты, с историей операций",
        response_description="Детальная информация по карте",
        tags=["GET"],
    )
    async def get_card(
        self, request: "Request", id_: UUID = query_id
    ) -> Optional[CardSchema]:
        return await request.app.store.card.get_card_by_id(id_card=id_)

    @card_route.get(
        "/get_all/",
        summary="Список карт",
        description="Список карт, по умолчанию возвращается 10 первых ",
        response_description="Список данных по картам, данных по транзакциям ",
        tags=["GET"],
    )
    async def get_all(
        self,
        request: "Request",
        series: Optional[int] = query_series,
        number: int = query_number,
        status: StatusCardEnum = query_status,
        create_date: date = query_create_date,
        expire_date: date = query_expire_date,
        page_size: int = query_page_size,
        page_number: int = query_page_number,
    ) -> list[CardSchema]:
        return await request.app.store.card.get_all(
            series=series,
            number=number,
            status=status,
            create_date=create_date,
            expire_date=expire_date,
            page_number=page_number,
            page_size=page_size,
        )

    @card_route.get("/test")
    async def test(self):
        1 / 0
        return {"status": "test success"}
