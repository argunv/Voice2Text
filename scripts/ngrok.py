import subprocess
import requests
import time
from config.settings import settings
import os
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR, filename="logs/ngrok.log")


async def run_ngrok() -> str:
    """Создание туннеля с помощью ngrok

    Raises:
        Exception: Если ngrok не установлен

    Returns:
        str: URL туннеля ngrok
    """
    await setup_ngrok()

    # Запуск ngrok
    logger.error(">>> Запуск ngrok...")
    ngrok_process = subprocess.Popen(
        ["ngrok", settings.NGROK_PROTOCOL, settings.NGROK_PORT],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    time.sleep(3)  # Ожидание запуска ngrok
    if ngrok_process.poll() is not None:  # Проверка завершения процесса
        raise Exception("Ngrok process failed to start")

    # Получение URL туннеля
    logger.error(">>> Получение URL туннеля...")
    response = requests.get("http://localhost:4040/api/tunnels")
    if response.status_code != 200:
        raise Exception("Could not get ngrok tunnels")

    tunnels = response.json().get("tunnels")
    if not tunnels:
        raise Exception("No tunnels found")

    public_url = tunnels[0].get("public_url")
    if not public_url:
        raise Exception("No public URL found")

    logger.error(f">>> Туннель ngrok запущен: {public_url}")
    return public_url


async def setup_ngrok() -> None:
    """Настройка ngrok"""
    logger.error(">>> Проверка наличия ngrok...")
    ngrok_path = subprocess.run(["which", "ngrok"], capture_output=True, text=True).stdout.strip()
    if not ngrok_path:
        raise Exception("Ngrok is not installed")

    logger.error(">>> Проверка наличия токена аутентификации...")
    if not getattr(settings, 'NGROK_TOKEN', None):
        raise Exception("Ngrok token is not provided")

    # проверка, нужно ли задавать токен аутентификации
    # NOTE: по умолчанию путь к конфигурационному файлу: 
    # /root/.config/ngrok/ngrok.yml
    config_path = "/root/.config/ngrok/ngrok.yml"

    logger.error(">>> Настройка ngrok...")
    # check if the file exists
    if not os.path.exists(config_path):
        # добавление токена аутентификации
        subprocess.run(["ngrok",
                        "config",
                        "add-authtoken",
                        settings.NGROK_TOKEN])
        logger.error(">>> Токен аутентификации добавлен!")
    logger.error(">>> Токен аутентификации уже добавлен!")

