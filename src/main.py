from fastapi import FastAPI

from src.routers.v1.notes import router as v1_notes_router

app = FastAPI()

app.include_router(v1_notes_router)
