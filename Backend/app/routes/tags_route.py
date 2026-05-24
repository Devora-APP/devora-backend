from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.schemas.tag import TagCreate, TagResponse
from app.services.tag_service import create_tag, get_tags

router = APIRouter(prefix="/tags", tags=["Tags"])


@router.post("/", response_model=TagResponse)
def create_new_tag(data: TagCreate, db: Session = Depends(get_db)):
    return create_tag(db, data)


@router.get("/", response_model=list[TagResponse])
def list_tags(db: Session = Depends(get_db)):
    return get_tags(db)