from datetime import datetime, time
from typing import Any

from card.models import CardModel, CardTransactionsModel
from sqlalchemy import and_, select
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy.sql.selectable import Select

# CardModel fields name
ID = CardModel.id.description
SERIES = CardModel.series.description  # noqa
NUMBER = CardModel.number.description  # noqa
CREATE_DATE = CardModel.create_date.description  # noqa
EXPIRE_DATE = CardModel.expire_date.description  # noqa
STATUS = CardModel.status.description  # noqa

# CardTransactionsModel fields name
ID_CARD = CardTransactionsModel.id_card.description
TRANSACTION_AMOUNT = CardTransactionsModel.transaction_amount.description  # noqa

PAGE_SIZE = "page_size"
PAGE_NUMBER = "page_number"


def get_comparisons(
    kwargs: dict[str, Any], fields_name: list[str]
) -> list[BinaryExpression]:
    comparisons = []
    for name, value in kwargs.items():
        if value and name in fields_name:
            if attr := getattr(CardModel, name, None):
                comparisons.append(attr == value)
    return comparisons  # noqa


def get_query(**kwargs) -> Select:
    query = select(
        CardModel.id,
        CardModel.series,
        CardModel.number,
        CardModel.create_date,
        CardModel.expire_date,
        CardModel.status,
    )
    comparisons = get_comparisons(
        kwargs,
        fields_name=[
            ID_CARD,
            SERIES,
            NUMBER,
            STATUS,
        ],
    )

    query = query.where(and_(*comparisons))
    if date := kwargs.get(CREATE_DATE):
        query = query.filter(
            and_(
                CardModel.create_date >= datetime.combine(date, time.min),
                CardModel.create_date <= datetime.combine(date, time.max),
            )
        )
    if date := kwargs.get(EXPIRE_DATE):
        query = query.filter(
            and_(
                CardModel.expire_date >= datetime.combine(date, time.min),
                CardModel.expire_date <= datetime.combine(date, time.max),
            )
        )
    query = query.order_by(CardModel.series, CardModel.number)
    if page_size := kwargs.get(PAGE_SIZE):
        query = query.offset((kwargs.get(PAGE_NUMBER) - 1) * page_size)
        query = query.limit(page_size)
    return query
