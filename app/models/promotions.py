from sqlalchemy import Column, Integer, String, Date
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, JSON, ForeignKey, UUID
import uuid
from app.core.timezone import DateTimeUTC, utc_now


class Promotion(Base):
    __tablename__ = "promotions"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String, nullable=False)
    thumb: Mapped[str] = mapped_column(String)
    merchant: Mapped[uuid.UUID] = mapped_column(ForeignKey("merchant.id", ondelete="CASCADE"))
    category = mapped_column(String)
    start_date = mapped_column(DateTimeUTC, default=utc_now)
    end_date = mapped_column(DateTimeUTC, default=utc_now)


class Merchant(Base):
    __tablename__ = "merchant"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String)

    promotions = relationship("Promotion", back_populates="merchant", cascade="all, delete")
