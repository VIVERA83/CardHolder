# from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
# from sqlalchemy.orm import declarative_base, sessionmaker
# from sqlalchemy import text
# import asyncio
# import csv
#
# DNS = "postgresql+asyncpg://kts_user:kts_pass@localhost:5432/kts"
#
# db = declarative_base()
#
# ""
#
# from icecream import ic
# async def dump_db():
#     engine: AsyncEngine = create_async_engine(DNS, echo=False, future=True)
#     session: AsyncSession = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
#
#     f = csv.writer(open('output.csv', 'wb'))
#     query = 'select * from cards'
#     async with session.begin() as session:
#         async for i in session.execute(text(query)):
#             ic(i)
#         f.writerows(await )
#
#     if engine:
#         await engine.dispose()
#
#
# if __name__ == "__main__":
#     asyncio.run(dump_db())
