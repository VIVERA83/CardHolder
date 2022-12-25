from datetime import date, datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field

from card.models import DurationEnum, StatusCardEnum
from card.utils import get_annotations_to_str


class BaseCardSchema(BaseModel):
    series: int = Field(
        default=None,
        description="Серия карты",
        ge=1,
        lt=9999,
        title="Серия карты",
        example=1253,
    )
    number: int = Field(
        default=None,
        description="Номер карты",
        ge=1,
        lt=9999,
        title="Номер карты",
        example=1253,
    )
    create_data: datetime = Field(
        default=None,
        description="Дата начала действия карты",
        title="Дата активации карты",
        example="2022-12-21",
    )
    expire_date: datetime = Field(
        default=None,
        description="Дата окончания действия карты",
        title="Дата окончания действия карты",
        example="2022-12-21",
    )
    status: StatusCardEnum = Field(
        default=None,
        description=f"Статус карты может быть одним из: {get_annotations_to_str(StatusCardEnum)}",
        title="Статус карты",
    )


class CardShortSchema(BaseCardSchema):
    pass


class CardTransactionsSchema(BaseModel):
    id: UUID = Field(
        description="уникальный `id` операции по карте, задается автоматически",
        title="Id операции",
    )
    transaction_amount: float = Field(
        default=1,
        description="Сумма операции по карте",
        ge=1,
        lt=1_000_000,
        title="Сумма операции",
        example=1200,
    )
    transaction_date: datetime = Field(
        description="Дата и время совершения операции, задается автоматически",
        title="Дата операции",
    )
    id_card: UUID = Field(
        description="уникальный `id` номер карты, задается автоматически",
        title="Id номер карты",
    )


class CardSchema(BaseCardSchema):
    id: UUID = Field(
        description="уникальный `id` номер карты, задается автоматически",
        title="Id номер карты",
    )
    card_transactions: list[CardTransactionsSchema] = Field(
        default=[],
        description="Список операций по карте согласно схеме `CardTransactionsSchema`",
        title="Список операций",
    )


class SearchSchema(BaseCardSchema):
    create_data: date = Field(
        default=None,
        description="Дата начала действия карты",
        title="Дата активации карты",
        example="2022-12-21",
    )
    expire_date: date = Field(
        default=None,
        description="Дата окончания действия карты",
        title="Дата окончания действия карты",
        example="2022-12-21",
    )

    page_number: int = Field(
        default=1,
        alias="page[number]",
        title="Какие то страницы",
        description="Вернет записи начина с указанной страницы, то есть page_size*page_number",
        gt=0,
        example=1,
    )
    page_size: int = Field(
        default=10,
        alias="page[size]",
        title="Какие то страницы",
        description="Кол-во записей которое будет возвращены в ответе, по умолчанию 100",
        gt=0,
        example=100,
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
    series: int = Field(
        description="Серия карты",
        ge=1,
        lt=100_00,
        title="Серия карты",
        example=1253,
    )
    duration: "DurationEnumStr" = Field(
        default=DurationEnum.month,
        description=f"Срок годности карты с момента создания: {get_annotations_to_str(DurationEnumStr)}",
        title="Срок годности",
        example=f"{DurationEnumStr.month}",
    )
