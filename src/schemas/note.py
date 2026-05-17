from src.schemas.common import BaseSchema, BaseResponse


class NoteSchema(BaseSchema):
    title: str
    body: str


class NoteResponseSchema(NoteSchema, BaseResponse):
    pass
