import hashlib


def generate_file_hash(file_path: str) -> str:
    """
    Генерирует хэш для указанного файла.
    """
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()
