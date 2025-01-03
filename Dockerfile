# Базовый образ
FROM python:3.10

# Установка необходимых инструментов
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN pip install poetry

# Установка Python-зависимостей
WORKDIR /app
COPY pyproject.toml poetry.lock /app/

# Отключение виртуальных окружений и установка зависимостей
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

# Установка Whisper и PyTorch (без использования Poetry)
RUN pip install --index-url=https://download.pytorch.org/whl/cpu torch==2.3.0 \
    torchaudio==2.3.0 torchvision==0.18.0
RUN pip install openai-whisper==20231117

# Копирование проекта
COPY . /app/

# Команда запуска
CMD ["sh", "scripts/startup.sh"]
