"""Модуль для работы с MinIO через REST API.

Описание модуля:
Модуль содержит роутер для работы с MinIO через REST API.
Роутер содержит следующие методы:
- upload_file: загрузка файла в MinIO;
- list_files: получение списка файлов в MinIO;
- download_file: скачивание файла из MinIO;
- delete_file: удаление файла из MinIO.

Пример использования:
1. Запустите FastAPI приложение:
uvicorn app.api.rest.main:app --reload
2. Перейдите по адресу http://
3. Выполните запросы к API.

Почему модуль не внедрен в основное приложение?
Бот использует SDK boto3 для работы с MinIO, а не REST API, 
что делает этот модуль избыточным для бота.
"""
from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from app.core.minio_client import get_minio_client
from config.settings import settings
import io

router = APIRouter()

# Получение клиента MinIO
minio_client = get_minio_client()

@router.post("/upload/")
async def upload_file(file: UploadFile):
    """
    Загрузка файла в MinIO
    """
    try:
        bucket_name = settings.MINIO_BUCKET_NAME
        file_data = await file.read()
        minio_client.put_object(
            bucket_name, file.filename, io.BytesIO(file_data), len(file_data)
        )
        return {"message": f"Файл {file.filename} успешно загружен."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list/")
async def list_files():
    """
    Получение списка файлов в MinIO
    """
    try:
        bucket_name = settings.MINIO_BUCKET_NAME
        objects = minio_client.list_objects(bucket_name)
        file_list = [obj.object_name for obj in objects]
        return {"files": file_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download/{filename}")
async def download_file(filename: str):
    """
    Скачивание файла из MinIO
    """
    try:
        bucket_name = settings.MINIO_BUCKET_NAME
        response = minio_client.get_object(bucket_name, filename)
        return StreamingResponse(response, media_type="application/octet-stream")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Файл {filename} не найден: {e}")


@router.delete("/delete/{filename}")
async def delete_file(filename: str):
    """
    Удаление файла из MinIO
    """
    try:
        bucket_name = settings.MINIO_BUCKET_NAME
        minio_client.remove_object(bucket_name, filename)
        return {"message": f"Файл {filename} успешно удалён."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
