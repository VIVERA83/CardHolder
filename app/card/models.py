import enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, TIMESTAMP, Enum, FLOAT, ForeignKey
from datetime import datetime, timedelta

from store.database.sqlalchemy_base import db
from uuid import uuid4


class StatusCardEnum(enum.Enum):
    not_active: str = "not_active"
    active: str = "active"
    expired: str = "expired"


class CardModel(db):
    __tablename__ = "cards"  # noqa

    id: uuid4 = Column(UUID(as_uuid=True), default=uuid4)
    series: int = Column(Integer, primary_key=True)
    number: int = Column(Integer, primary_key=True)
    create_data: datetime = Column(TIMESTAMP, default=datetime.now())
    expire_date: datetime = Column(TIMESTAMP, default=datetime.now() + timedelta(days=30))
    status: str = Column(Enum(StatusCardEnum), default=StatusCardEnum.not_active)
    card_transactions: list["CardTransactionsModel"] = relationship(
        "CardTransactionsModel",
        backref="cards",
        cascade="all, delete",
        passive_deletes=True,
    )


class CardTransactionsModel(db):
    __tablename__ = "card_transactions"  # noqa

    id: uuid4 = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    id_card: uuid4 = Column(UUID, ForeignKey("cards.series", ondelete="CASCADE"), nullable=False)
    transaction_amount = Column(FLOAT, nullable=False)
    transaction_date = Column(TIMESTAMP, nullable=False)
