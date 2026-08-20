from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime
from datetime import datetime

class Base(DeclarativeBase):
    pass

class DocumentModel(Base):

    __tablename__ = "documents"

    id : Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    filename : Mapped[str] = mapped_column(String, nullable=False)
    source_path : Mapped[str] = mapped_column(String, nullable=False)
    total_chunks : Mapped[int] = mapped_column(Integer)
    total_pages : Mapped[int] = mapped_column(Integer)
    uploaded_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)