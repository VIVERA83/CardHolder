from datetime import datetime
from functools import wraps
from uuid import UUID

from base.base_accessor import BaseAccessor
from card.models import CardModel, CardTransactionsModel, DurationEnum, StatusCardEnum
from sqlalchemy import and_, delete, insert, select, update
from sqlalchemy.engine import ChunkedIteratorResult, CursorResult
from sqlalchemy.orm import selectinload

from .utils import (
    CREATE_DATE,
    EXPIRE_DATE,
    ID,
    ID_CARD,
    NUMBER,
    SERIES,
    STATUS,
    TRANSACTION_AMOUNT,
    get_comparisons,
    get_query,
)


class CardAccessor(BaseAccessor):
    @staticmethod
    def _card_expiration(func):
        @wraps(func)
        async def inner(cls: "CardAccessor", **kwargs):
            comparisons = get_comparisons(
                kwargs,
                [
                    ID,
                    SERIES,
                    NUMBER,
                    CREATE_DATE,
                    EXPIRE_DATE,
                    STATUS,
                ],
            )
            comparisons.append(CardModel.expire_date < datetime.now())  # noqa
            comparisons.append(CardModel.status != StatusCardEnum.expired)  # noqa
            async with cls.app.database.session.begin() as session:
                query = (
                    update(CardModel)
                    .where(and_(*comparisons))
                    .values(status=StatusCardEnum.expired)
                    .returning(CardModel)
                )
                await session.execute(query)
            return await func(cls, **kwargs)

        return inner

    async def create_cards(
        self, series: int, count: int, duration: DurationEnum
    ) -> list[dict]:
        """
        Create a list of cards.
        :param series:
        :param count:
        :param duration:
        :return: list of cards
        """
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
                            SERIES: card.series,
                            EXPIRE_DATE: card.expire_date,
                        }
                        for card in cards
                    ]
                )
                .returning(CardModel)
            )
            result: CursorResult = await session.execute(query)
            self.logger.info(" Create %s cards", result.unique().rowcount)
        return [i._asdict() for i in result.unique().all()]  # noqa

    @_card_expiration
    async def get_all(
        self,
        series: int = None,
        number: int = None,
        create_date: datetime = None,
        expire_date: datetime = None,
        status: StatusCardEnum = None,
        page_number: int = None,
        page_size: int = None,
    ) -> list[CardModel]:
        """
        Returns all cards by request parameters
        """
        async with self.app.database.session.begin() as session:
            query = get_query(
                series=series,
                number=number,
                create_date=create_date,
                expire_date=expire_date,
                status=status,
                page_number=page_number,
                page_size=page_size,
            )
            chang: ChunkedIteratorResult = await session.execute(query)
            return chang.unique().fetchall()  # noqa

    @_card_expiration
    async def create_transaction(
        self,
        id_card: UUID,
        amount: float,
    ) -> CardTransactionsModel:
        """
        Add a transaction record to the card
        """
        async with self.app.database.session.begin() as session:
            query = (
                insert(CardTransactionsModel)
                .values([{TRANSACTION_AMOUNT: amount, ID_CARD: id_card.hex}])
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
        """
        Updating data in the specified map
        """
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
        """
        Get Card by id
        """
        async with self.app.database.session.begin() as session:
            query = (
                select(CardModel)
                .options(selectinload(CardModel.card_transactions))
                .where(CardModel.id == id_card)
            )
            result = await session.execute(query)

            return result.unique().scalars().first()

    async def delete_card(
        self,
        id_card: UUID,
    ) -> CardModel:
        """
        Delete a card
        """
        async with self.app.database.session.begin() as session:
            query = (
                delete(CardModel)
                .options(selectinload(CardModel.card_transactions))
                .where(CardModel.id == id_card)
                .returning(CardModel)
            )
            result = await session.execute(query)
            return result.unique().first()
