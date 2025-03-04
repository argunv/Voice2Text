import os

import boto3
import requests

from botocore.exceptions import ClientError
from config.settings import settings

from app.core.logger import Logger


logger = Logger("minio_client").get_logger()


def get_minio_client():
    """
    Создаёт и возвращает MinIO клиент.
    """
    return boto3.client(
        's3',
        aws_access_key_id=settings.MINIO_ROOT_USER,
        aws_secret_access_key=settings.MINIO_ROOT_PASSWORD,
        endpoint_url=settings.MINIO_ENDPOINT
    )


def validate_file_name(file_name: str) -> bool:
    """
    Проверяет имя файла на допустимые символы.

    Args:
        file_name (str): Имя файла.

    Returns:
        bool: Результат проверки.
    """
    invalid_conditions = [
        not file_name,
        not file_name.isprintable(),
        "/" in file_name,
        "\\" in file_name,
        len(file_name) > 255,
        file_name.startswith("."),
        file_name.endswith("."),
        any(char in file_name for char in "~#%&*{}\\:<>?/+|\"'")
    ]
    return not any(invalid_conditions)


def upload_file_to_minio(file_url, file_name) -> dict[str]:
    """
    Скачивает файл по URL, сохраняет его локально и загружает в MinIO.

    Args:
        file_url (str): URL файла для загрузки.
        file_name (str): Имя файла для сохранения в MinIO.

    Returns:
        dict: JSON с данными про загруженный файл.

        - **file_name** (*str*): Имя файла.
        - **file_ext** (*str*): Расширение файла.
        - **file_size** (*int*): Размер файла.
        - **endpoint** (*str*): URL MinIO.
        - **bucket_name** (*str*): Имя бакета.

    Raises:
        ValueError: Если произошла ошибка при загрузке файла.
    """
    if not validate_file_name(file_name):
        raise ValueError(f"Недопустимое имя файла: '{file_name}'")

    client = get_minio_client()
    bucket_name = settings.MINIO_BUCKET_NAME

    ensure_bucket_exists(client, bucket_name)

    # Локальный путь для временного хранения файла
    local_dir = "/tmp/voice"
    os.makedirs(local_dir, exist_ok=True)  # Создаем директорию, если её нет

    # Полный путь к файлу
    local_file = os.path.join(local_dir, os.path.basename(file_name))

    try:
        # Скачиваем файл
        response = requests.get(file_url, timeout=10)
        response.raise_for_status()
        with open(local_file, "wb") as f:
            f.write(response.content)
    except requests.RequestException as e:
        raise ValueError(f"Ошибка загрузки файла с URL {file_url}: {e}")

    try:
        # Загружаем файл в MinIO
        client.upload_file(local_file, bucket_name, os.path.basename(file_name))
    except ClientError as e:
        raise ValueError(f"Ошибка загрузки файла в MinIO: {e}")

    # Возвращаем URL загруженного файла
    # return f"{settings.MINIO_ENDPOINT}/{bucket_name}/{os.path.basename(file_name)}"

    # Возвращаем JSON с данными про загруженный файл
    answer = {
        "file_name": os.path.basename(file_name),
        "file_ext": os.path.splitext(file_name)[1],
        "file_size": os.path.getsize(local_file),
        "endpoint": settings.MINIO_ENDPOINT,
        "bucket_name": settings.MINIO_BUCKET_NAME
    }

    return answer

def download_file_from_minio(file_name):
    """
    Скачивает файл из MinIO.

    Args:
        file_name (str): Имя файла для скачивания.

    Returns:
        str: Локальный путь к скачанному файлу.
    """
    client = get_minio_client()
    bucket_name = settings.MINIO_BUCKET_NAME

    local_file = f"/tmp/{file_name}"
    try:
        client.download_file(bucket_name, file_name, local_file)
    except ClientError as e:
        raise ValueError(f"Ошибка загрузки файла из MinIO: {e}")

    return local_file


def ensure_bucket_exists(client, bucket_name):
    """
    Проверяет наличие бакета в MinIO и создаёт его при необходимости.

    Args:
        client: MinIO клиент.
        bucket_name (str): Имя бакета.

    Raises:
        ValueError: Если не удалось проверить или создать бакет.
    """
    try:
        existing_buckets = client.list_buckets().get("Buckets", [])
        if not any(bucket["Name"] == bucket_name for bucket in existing_buckets):
            client.create_bucket(Bucket=bucket_name)
    except ClientError as e:
        raise ValueError(f"Ошибка при проверке или создании бакета '{bucket_name}': {e}")
