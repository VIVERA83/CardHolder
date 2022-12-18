import enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, TIMESTAMP, Enum, FLOAT, ForeignKey
from datetime import datetime, timedelta
from dataclasses import dataclass
from store.database.sqlalchemy_base import db
from uuid import uuid4


class StatusCardEnum(enum.Enum):
    not_active: str = "not_active"
    active: str = "active"
    expired: str = "expire_data"


class DurationEnum(enum.Enum):
    year: datetime = timedelta(days=365)
    six_months: datetime = timedelta(days=180)
    month: datetime = timedelta(days=30)


@dataclass
class CardModel(db):
    __tablename__ = "cards"  # noqa

    id: uuid4 = Column(UUID(as_uuid=True), default=uuid4, unique=True)
    series: int = Column(Integer, primary_key=True)
    number: int = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    create_data: datetime = Column(TIMESTAMP, default=datetime.now())
    expire_date: datetime = Column(TIMESTAMP, default=datetime.now() + DurationEnum.month.value)
    status: str = Column(Enum(StatusCardEnum), default=StatusCardEnum.not_active)
    card_transactions: list["CardTransactionsModel"] = relationship(
        "CardTransactionsModel",
        backref="cards",
        cascade="all, delete",
        passive_deletes=True,
    )


@dataclass
class CardTransactionsModel(db):
    __tablename__ = "card_transactions"  # noqa

    id: uuid4 = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    transaction_amount = Column(FLOAT, nullable=False)
    transaction_date = Column(TIMESTAMP, nullable=False)

    id_card: uuid4 = Column(UUID(as_uuid=True), ForeignKey("cards.id", ondelete="CASCADE"), nullable=False)

