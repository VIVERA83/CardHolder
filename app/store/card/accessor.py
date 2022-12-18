from base.base_accessor import BaseAccessor


class CardAccessor(BaseAccessor):
    async def create_cards(self, series: int, count: int):
        return {"series": series, "count": count}
