from datetime import datetime

from pydantic import BaseModel


class BaseSchema(BaseModel):
    pass

class BaseResponse(BaseModel):
    id: int
    created_at: datetime
