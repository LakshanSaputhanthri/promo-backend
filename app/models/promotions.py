from sqlalchemy import Column, Integer, String, Date
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, JSON, ForeignKey, UUID
import uuid
from app.core.timezone import DateTimeUTC, utc_now


class Promotion(Base):
    __tablename__ = "promotions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String, nullable=False)
    merchant: Mapped[str] = mapped_column(String, nullable=False)  # just store name
    thumb: Mapped[str] = mapped_column(String, nullable=True)
    card_type: Mapped[str] = mapped_column(String, nullable=False)
    valid_to: Mapped[str] = mapped_column(String, nullable=True)
