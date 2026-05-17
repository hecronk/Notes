import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.models.common import BaseModel
from src.core.database.db import Base


class Note(BaseModel, Base):

    __tablename__ = "notes"

    title: Mapped[str] = mapped_column(sa.String(255))
    body: Mapped[str] = mapped_column(sa.Text)
