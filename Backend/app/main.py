from fastapi import FastAPI
from app.core.db import engine
from fastapi.middleware.cors import CORSMiddleware
from app.core.base import Base
from app.models import user
from app.routes import (
    answers_route,
    auth_route,
    comments_route,
    questions_route,
    tags_route,
    users_route,
    votes_route
)

from app.routes import ai

app = FastAPI(title="Devora Backend")

app.include_router(ai.router)

app.include_router(auth_route.router)
app.include_router(users_route.router)
app.include_router(questions_route.router)
app.include_router(answers_route.router)
app.include_router(votes_route.router)
app.include_router(tags_route.router)
app.include_router(comments_route.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Devora backend is running."}