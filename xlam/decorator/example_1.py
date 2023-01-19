from asyncio import run, sleep
from functools import wraps

from icecream import ic


class Example:
    def __init__(self):
        self.db = "Database"

    @staticmethod
    def decorator(self):
        @wraps(self)
        def inner(*args, **kwargs):
            ic(self, *args, **kwargs)
            result = self(*args)
            return result

        return inner

    @decorator
    async def set_data(self, data: str):
        result = await sleep(1, result="hello")
        ic(result)
        return self.db + data

    def __str__(self):
        return self.__class__.__name__

    async def t(self):
        return await self.set_data(" 111111")

    __repr__ = __str__


if __name__ == "__main__":
    example = Example()
    r = run(example.t())
    ic(r)


# if
# async def inner(
#         **kwargs):
#     async with ses.app.database.session.begin() as session:
#         query = get_query(**kwargs)
#         query = query.where(CardModel.expire_date < datetime.now())
#         query = update(CardModel).values(status=StatusCardEnum.expired).returning(CardModel)
#         result = await session.execute(query)
#         ic(result.unique().first())
#
#     return await func()


# def get_query(
#         id_card: UUID = None,
#         series: int = None,
#         number: int = None,
#         create_data: datetime = None,
#         expire_date: datetime = None,
#         status: StatusCardEnum = None,
#         page_number: int = None,
#         page_size: int = None,
# ) -> Select:
#     query = select(
#         CardModel.series,
#         CardModel.number,
#         CardModel.create_data,
#         CardModel.expire_date,
#         CardModel.status,
#     )
#     if id_card:
#         query = query.where(CardModel.id == id_card)
#     if series:
#         query = query.where(CardModel.series == series)
#     if number:
#         query = query.where(CardModel.number == number)
#     if create_data:
#         query = query.where(
#             and_(
#                 CardModel.create_data >= datetime.combine(create_data, time.min),
#                 CardModel.create_data <= datetime.combine(create_data, time.max),
#             )
#         )
#     if expire_date:
#         query = query.filter(
#             and_(
#                 CardModel.expire_date >= datetime.combine(expire_date, time.min),
#                 CardModel.expire_date <= datetime.combine(expire_date, time.max),
#             )
#         )
#     if status:
#         query = query.where(CardModel.status == status)
#     query = query.order_by(CardModel.series, CardModel.number)
#     if page_size:
#         query = query.offset((page_number - 1) * page_size)
#     if page_size:
#         query = query.limit(page_size)
#     return query
