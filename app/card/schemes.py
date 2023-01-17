from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field

from card.models import DurationEnum, StatusCardEnum
from card.query_params import (
    query_create_date,
    query_expire_date,
    query_id,
    query_number,
    query_series,
    query_status,
)
from card.utils import get_annotations_to_str


class BaseCardSchema(BaseModel):
    series: int = query_series
    number: int = query_number
    create_data: datetime = query_create_date
    expire_date: datetime = query_expire_date
    status: StatusCardEnum = query_status


class CardShortSchema(BaseCardSchema):
    id: UUID = query_id


class CardTransactionsSchema(BaseModel):
    id: UUID = Field(
        description="уникальный `id` операции по карте, задается автоматически",
        title="Id операции",
    )
    transaction_amount: float = Field(
        default=1,
        description="Сумма операции по карте",
        ge=1,
        lt=10000000000000,
        title="Сумма операции",
        example=1200,
    )
    transaction_date: datetime = Field(
        description="Дата и время совершения операции, задается автоматически",
        title="Дата операции",
        example="2023-01-21",
    )

    id_card: UUID = Field(
        description="уникальный `id` номер карты, задается автоматически",
        title="Id номер карты",
        example="a17b2315-5bb8-40d3-8d8a-2d48b6c3144e",
    )


class CardSchema(BaseCardSchema):
    id_: UUID = query_id
    card_transactions: list[CardTransactionsSchema] = Field(
        default=[],
        description="Список операций по карте согласно схеме `CardTransactionsSchema`",
        title="Список операций",
    )


class DurationEnumStr(Enum):
    year: str = "year"
    six_months: str = "six_months"
    month: str = "month"

    def modified(self) -> DurationEnum:
        data = {
            self.value == DurationEnum.year.name: DurationEnum.year,
            self.value == DurationEnum.month.name: DurationEnum.month,
            self.value == DurationEnum.six_months.name: DurationEnum.six_months,
        }
        return data.get(True)


class CreateCardSchema(BaseModel):
    count: int = Field(title="Количество генерируемых карт", ge=1, lt=100, example=10)
    series: int = query_series
    duration: "DurationEnumStr" = Field(
        default=DurationEnumStr.month,
        description=f"Срок годности карты с момента создания: {get_annotations_to_str(DurationEnumStr)}",
        title="Срок годности",
        example=f"{DurationEnumStr.month.value}",
    )
