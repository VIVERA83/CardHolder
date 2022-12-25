from functools import wraps
from datetime import datetime, time
from typing import Any
from uuid import UUID

from sqlalchemy import and_, delete, insert, select, update
from sqlalchemy.sql.selectable import Select
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy.engine import ChunkedIteratorResult, CursorResult
from sqlalchemy.orm import selectinload

from base.base_accessor import BaseAccessor
from card.models import CardModel, CardTransactionsModel, DurationEnum, StatusCardEnum

from icecream import ic


class CardAccessor(BaseAccessor):
    @staticmethod
    def _card_expiration(func):
        @wraps(func)
        async def inner(cls: "CardAccessor", **kwargs):
            ands = await cls.get_comparisons(kwargs)
            async with cls.app.database.session.begin() as session:
                query = (
                    update(CardModel)
                    .where(and_(*ands))
                    .values(status=StatusCardEnum.expired)
                    .returning(CardModel)
                )
                r = await session.execute(query)
                ic(r.unique().fetchall())
            result = await func(cls, **kwargs)
            return result

        return inner

    @staticmethod
    async def get_comparisons(kwargs: dict[str, Any]) -> list[BinaryExpression]:
        ands = []
        for name, value in kwargs.items():
            if value and name in [
                "id_card",
                "series",
                "number",
                "create_data",
                "expire_date",
                "status",
            ]:
                if attr := getattr(CardModel, name, None):
                    ands.append(attr == value)
        ands.append(CardModel.expire_date < datetime.now())
        ands.append(CardModel.status != StatusCardEnum.expired)
        return ands  # noqa

    async def create_cards(
        self, series: int, count: int, duration: DurationEnum
    ) -> list[dict]:
        cards = [
            CardModel(
                series=series,
                expire_date=datetime.now() + duration.value,
                status=StatusCardEnum.not_active.value,
            )
            for _ in range(count)
        ]

        async with self.app.database.session.begin() as session:
            query = (
                insert(CardModel)
                .values(
                    [
                        {
                            "series": card.series,
                            "expire_date": card.expire_date,
                        }
                        for card in cards
                    ]
                )
                .returning(CardModel)
            )
            result: CursorResult = await session.execute(query)
        return [i._asdict() for i in result.unique().all()]  # noqa

    @_card_expiration
    async def get_cards(
        self,
        series: int = None,
        number: int = None,
        create_data: datetime = None,
        expire_date: datetime = None,
        status: StatusCardEnum = None,
        page_number: int = None,
        page_size: int = None,
    ) -> list[CardModel]:
        async with self.app.database.session.begin() as session:
            query = get_query(
                None,
                series,
                number,
                create_data,
                expire_date,
                status,
                page_number,
                page_size,
            )
            chang: ChunkedIteratorResult = await session.execute(query)
            return chang.unique().fetchall()  # noqa

    @_card_expiration
    async def get_card(self, series: int, number: int) -> CardModel:
        async with self.app.database.session.begin() as session:
            query = (
                select(CardModel)
                .options(selectinload(CardModel.card_transactions))
                .where(and_(CardModel.series == series, CardModel.number == number))
            )
            result: ChunkedIteratorResult = await session.execute(query)
            return result.scalars().first()

    @_card_expiration
    async def create_transaction(
        self,
        id_card: UUID,
        amount: float,
    ) -> CardTransactionsModel:
        async with self.app.database.session.begin() as session:
            query = (
                insert(CardTransactionsModel)
                .values([{"transaction_amount": amount, "id_card": id_card.hex}])
                .returning(CardTransactionsModel)
            )
            result = await session.execute(query)
            return result.unique().first()

    @_card_expiration
    async def update_card_status(
        self,
        id_card: UUID,
        status: StatusCardEnum,
    ) -> CardModel:
        async with self.app.database.session.begin() as session:
            query = (
                update(CardModel)
                .where(CardModel.id == id_card)
                .values(status=status)
                .returning(CardModel)
            )
            result = await session.execute(query)
            return result.unique().first()

    @_card_expiration
    async def get_card_by_id(
        self,
        id_card: UUID,
    ) -> CardModel:
        async with self.app.database.session.begin() as session:
            query = (
                select(CardModel)
                .options(selectinload(CardModel.card_transactions))
                .where(CardModel.id == id_card)
            )
            result = await session.execute(query)
            return result.unique().first()

    async def delete_card(
        self,
        id_card: UUID,
    ) -> CardModel:
        async with self.app.database.session.begin() as session:
            query = (
                delete(CardModel)
                .options(selectinload(CardModel.card_transactions))
                .where(CardModel.id == id_card)
                .returning(CardModel)
            )
            result = await session.execute(query)
            return result.unique().first()


def get_query(
    id_card: UUID = None,
    series: int = None,
    number: int = None,
    create_data: datetime = None,
    expire_date: datetime = None,
    status: StatusCardEnum = None,
    page_number: int = None,
    page_size: int = None,
) -> Select:
    query = select(
        CardModel.series,
        CardModel.number,
        CardModel.create_data,
        CardModel.expire_date,
        CardModel.status,
    )
    if id_card:
        query = query.where(CardModel.id == id_card)
    if series:
        query = query.where(CardModel.series == series)
    if number:
        query = query.where(CardModel.number == number)
    if create_data:
        query = query.where(
            and_(
                CardModel.create_data >= datetime.combine(create_data, time.min),
                CardModel.create_data <= datetime.combine(create_data, time.max),
            )
        )
    if expire_date:
        query = query.filter(
            and_(
                CardModel.expire_date >= datetime.combine(expire_date, time.min),
                CardModel.expire_date <= datetime.combine(expire_date, time.max),
            )
        )
    if status:
        query = query.where(CardModel.status == status)
    query = query.order_by(CardModel.series, CardModel.number)
    if page_size:
        query = query.offset((page_number - 1) * page_size)
    if page_size:
        query = query.limit(page_size)
    return query
