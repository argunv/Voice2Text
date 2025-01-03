from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine

from config.settings import settings

engine = create_engine(f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}")
metadata = MetaData()

transcriptions = Table(
    'transcriptions',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, nullable=False),
    Column('transcription', String, nullable=False),
)

def save_transcription(user_id, transcription):
    with engine.connect() as conn:
        conn.execute(transcriptions.insert().values(user_id=user_id, transcription=transcription))
