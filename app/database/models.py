from sqlalchemy import Column, Integer, BigInteger, String, Text, DateTime
from app.database.database import Base
from sqlalchemy.sql import func


class VoiceMessage(Base):
    __tablename__ = "voice_messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False, index=True)
    file_url = Column(String, nullable=False)
    transcription = Column(Text, nullable=True)
    status = Column(String(20), nullable=False, server_default="pending")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)


class FloodControl(Base):
    __tablename__ = "flood_control"

    user_id = Column(BigInteger, primary_key=True)
    last_message = Column(DateTime, nullable=False)
    message_count = Column(Integer, nullable=False, server_default="0")


class Transcription(Base):
    __tablename__ = "transcriptions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False, index=True)
    transcription = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
