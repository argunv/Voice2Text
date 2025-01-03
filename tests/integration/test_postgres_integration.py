from app.database.database import Base, SessionLocal, engine
from app.database.models import Transcription


def test_postgres_integration():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()

    transcription = Transcription(user_id=1, transcription="Test")
    session.add(transcription)
    session.commit()

    result = session.query(Transcription).filter_by(user_id=1).first()
    assert result.transcription == "Test"

    session.close()
    Base.metadata.drop_all(bind=engine)
