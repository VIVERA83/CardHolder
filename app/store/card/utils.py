from typing import Any
from sqlalchemy.sql.selectable import Select
from sqlalchemy.sql.elements import BinaryExpression
from card.models import CardModel
from sqlalchemy import and_, select
from datetime import datetime, time


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
        CardModel.series,
        CardModel.number,
        CardModel.create_data,
        CardModel.expire_date,
        CardModel.status,
    )
    comparisons = get_comparisons(
        kwargs,
        fields_name=[
            "id_card",
            "series",
            "number",
            "status",
        ],
    )

    query = query.where(and_(*comparisons))
    if date := kwargs.get("create_data"):
        query = query.filter(
            and_(
                CardModel.create_data >= datetime.combine(date, time.min),
                CardModel.create_data <= datetime.combine(date, time.max),
            )
        )
    if date := kwargs.get("expire_date"):
        query = query.filter(
            and_(
                CardModel.expire_date >= datetime.combine(date, time.min),
                CardModel.expire_date <= datetime.combine(date, time.max),
            )
        )
    query = query.order_by(CardModel.series, CardModel.number)
    if page_size := kwargs.get("page_size"):
        query = query.offset((kwargs.get("page_number") - 1) * page_size)
        query = query.limit(page_size)
    return query
