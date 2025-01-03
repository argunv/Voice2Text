import os

import boto3
import requests

from config.settings import settings


def get_minio_client():
    return boto3.client(
        's3',
        aws_access_key_id=settings.MINIO_ROOT_USER,
        aws_secret_access_key=settings.MINIO_ROOT_PASSWORD,
        endpoint_url=settings.MINIO_ENDPOINT
    )


def upload_file_to_minio(file_url, file_name):
    client = get_minio_client()
    bucket_name = settings.MINIO_BUCKET_NAME

    ensure_bucket_exists(client, bucket_name)

    # Создаем локальный путь
    local_dir = "/tmp/voice"
    os.makedirs(local_dir, exist_ok=True)  # Создаем директорию, если её нет

    # Полный путь к файлу
    local_file = os.path.join(local_dir, os.path.basename(file_name))

    # Скачиваем файл
    response = requests.get(file_url)
    response.raise_for_status()  # Проверяем успешность запроса
    with open(local_file, "wb") as f:
        f.write(response.content)

    # Загружаем файл в Minio
    client.upload_file(local_file, bucket_name, os.path.basename(file_name))

    # Возвращаем URL файла
    return f"{settings.MINIO_ENDPOINT}/{bucket_name}/{os.path.basename(file_name)}"


def download_file_from_minio(file_url):
    client = get_minio_client()
    bucket_name = settings.MINIO_BUCKET_NAME
    file_name = file_url.split("/")[-1]

    local_file = f"/tmp/{file_name}"
    client.download_file(bucket_name, file_name, local_file)

    return local_file


def ensure_bucket_exists(client, bucket_name):
    """
    Проверяет наличие бакета в Minio и создает его, если отсутствует.
    """
    try:
        buckets = client.list_buckets()["Buckets"]
        bucket_names = [bucket["Name"] for bucket in buckets]
        if bucket_name not in bucket_names:
            client.create_bucket(Bucket=bucket_name)
    except KeyError as e:
        raise ValueError(f"Не удалось получить список бакетов: {e}")
    except Exception as e:
        raise ValueError(f"Ошибка при проверке бакета: {e}")