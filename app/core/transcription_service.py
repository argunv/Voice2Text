from pathlib import Path

import torch
import whisper

from config.settings import settings

from app.core.logger import Logger


logger = Logger("transcription_service").get_logger()

# Конфигурация модели
MODEL_NAME = settings.WHISPER_MODEL or "small"
MODEL_PATH = Path(f"{settings.MODELS_DIR}/{MODEL_NAME}.pt")


def ensure_model_exists(model_name: str, model_path: Path):
    """
    Проверяет наличие модели и скачивает её, если отсутствует.
    """
    if not model_path.exists():
        logger.error(f"Модель {model_name} отсутствует, начинаем загрузку...")
        model = whisper.load_model(model_name)
        model.save(model_path)  # Сохраняем модель
        logger.error(f"Модель {model_name} загружена. Путь: {model_path}.")
    logger.error(f"Модель {model_name} уже существует. Путь: {model_path}.")


# Проверяем и загружаем модель
ensure_model_exists(MODEL_NAME, MODEL_PATH)

# Загружаем модель Whisper
logger.error(f"Загрузка модели {MODEL_NAME} из {MODEL_PATH}...")
model = whisper.load_model(MODEL_PATH)
logger.error(f"Модель {MODEL_NAME} успешно загружена.")


def transcribe_audio(file_path):
    """
    Транскрибирует аудиофайл с использованием модели Whisper.
    """
    logger.error(f"Начало транскрипции файла: {file_path}")
    result = model.transcribe(file_path)
    logger.error(f"Транскрипция завершена: {result['text']}")
    return result["text"]
