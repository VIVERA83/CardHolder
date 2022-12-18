from base.base_accessor import BaseAccessor
from card.models import CardModel, DurationEnum, StatusCardEnum
from datetime import datetime, timedelta


class CardAccessor(BaseAccessor):
    async def create_cards(self, series: int, count: int, duration: DurationEnum):
        async with self.app.database.session.begin() as session:
            cards = [
                CardModel(series=series,
                          expire_date=datetime.now() + duration.value,
                          status=StatusCardEnum.not_active.value)
                for _ in range(count)]
            session.add_all(cards)
            await session.commit()
        return {"series": series, "count": count}
