"""create voice_messages table

Revision ID: f99f593582bd
Revises: 
Create Date: 2024-12-24 07:26:24.164423

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f99f593582bd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Создание таблицы для голосовых сообщений
    op.create_table(
        'voice_messages',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.BigInteger, nullable=False, index=True),
        sa.Column('file_url', sa.String, nullable=False),
        sa.Column('transcription', sa.Text, nullable=True),  # Добавлено для хранения расшифровки
        sa.Column('status', sa.String(20), nullable=False, server_default='pending'),  # Статус обработки
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False)
    )
    
    # Создание таблицы для контроля флуда
    op.create_table(
        'flood_control',
        sa.Column('user_id', sa.BigInteger, primary_key=True),
        sa.Column('last_message', sa.DateTime, nullable=False),  # Последнее сообщение пользователя
        sa.Column('message_count', sa.Integer, nullable=False, server_default="0")  # Количество сообщений
    )

    # Создание таблицы для транскрипций
    op.create_table(
        'transcriptions',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.BigInteger, nullable=False, index=True),
        sa.Column('transcription', sa.Text, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False)
    )



def downgrade():
    # Удаление таблицы flood_control
    op.drop_table('flood_control')
    
    # Удаление таблицы voice_messages
    op.drop_table('voice_messages')

    # Удаление таблицы transcriptions
    op.drop_table('transcriptions')
