from typing import Optional
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column


class BaseModel(object):

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(sa.DateTime, default=sa.func.now(), server_default=sa.func.now())
