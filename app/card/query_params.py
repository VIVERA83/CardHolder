from datetime import datetime
from uuid import UUID

from fastapi import Query

from card.models import StatusCardEnum
from card.utils import get_annotations_to_str

query_id: UUID = Query(
    default=None,
    alias="id",
    description="уникальный `id` номер карты, задается автоматически",
    title="Id номер карты",
    example="a17b2315-5bb8-40d3-8d8a-2d48b6c3144e",
)
query_series: int = Query(
    default=None,
    description="Серия карты",
    ge=1,
    lt=9999,
    title="Серия карты",
    example=1253,
)
query_number: int = Query(
    default=None,
    description="Номер карты",
    ge=1,
    lt=9999,
    title="Номер карты",
    example=1253,
)
query_create_date: datetime = Query(
    default=None,
    description="Дата начала действия карты",
    title="Дата активации карты",
    example="2022-12-21",
)
query_expire_date: datetime = Query(
    default=None,
    description="Дата окончания действия карты",
    title="Дата окончания действия карты",
    example="2022-12-21",
)
query_status: StatusCardEnum = Query(
    default=None,
    description=f"Статус карты может быть одним из: {get_annotations_to_str(StatusCardEnum)}",
    title="Статус карты",
)

query_page_number: int = Query(
    default=1,
    alias="page[number]",
    title="Какие то страницы",
    description="Вернет записи начина с указанной страницы, то есть page_size*page_number",
    gt=0,
    example=1,
)

query_page_size: int = Query(
    default=10,
    alias="page[size]",
    title="Какие то страницы",
    description="Кол-во записей которое будет возвращены в ответе, по умолчанию 100",
    gt=0,
    example=100,
)
