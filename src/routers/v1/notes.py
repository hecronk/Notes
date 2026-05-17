from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException

from src.core.database.db import get_session
from src.core.database.models import Note
from src.schemas.note import NoteSchema, NoteResponseSchema

router = APIRouter(prefix="/api/v1/notes", tags=["Notes"])


@router.get("/", response_model=list[NoteResponseSchema], status_code=status.HTTP_200_OK,)
async def get_notes(
        session: AsyncSession = Depends(get_session),
):
    notes_query = select(Note).where(Note.body.isnot(None))
    result = await session.execute(notes_query)
    notes = result.scalars().all()
    return notes


@router.get("/{note_id}", response_model=NoteResponseSchema, status_code=status.HTTP_200_OK,)
async def get_note(
        note_id: int,
        session: AsyncSession = Depends(get_session),
):
    note = await session.get(Note, note_id)
    if note:
        return note
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")


@router.post("/", response_model=NoteResponseSchema, status_code=status.HTTP_201_CREATED,)
async def create_note(
        note_schema: NoteSchema,
        session: AsyncSession = Depends(get_session),
):
    note_data = note_schema.model_dump()
    note = Note(**note_data)
    session.add(note)
    await session.commit()
    await session.refresh(note)
    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT,)
async def delete_note(
        note_id: int,
        session: AsyncSession = Depends(get_session),
):
    note = await session.get(Note, note_id)
    await session.delete(note)
    await session.commit()
