from sqlalchemy import Column, ForeignKey, Integer, String

from app.database.database import Base


class Transcription(Base):
    __tablename__ = "transcriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    transcription = Column(String, nullable=False)
