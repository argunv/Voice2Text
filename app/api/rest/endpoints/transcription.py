from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.database.models import Transcription
from app.database.schema import Transcription as TranscriptionSchema

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/transcriptions/{user_id}", response_model=list[TranscriptionSchema])
def read_transcriptions(user_id: int, db: Session = Depends(get_db)):
    transcriptions = db.query(Transcription).filter(Transcription.user_id == user_id).all()
    if not transcriptions:
        raise HTTPException(status_code=404, detail="Transcriptions not found")
    return transcriptions
