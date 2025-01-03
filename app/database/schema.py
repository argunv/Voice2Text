from pydantic import BaseModel


class TranscriptionCreate(BaseModel):
    user_id: int
    transcription: str

class Transcription(BaseModel):
    id: int
    user_id: int
    transcription: str

    class Config:
        orm_mode = True
