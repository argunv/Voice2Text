import subprocess
import requests
import time
import os
from config.settings import settings
from app.core.logger import Logger


logger = Logger("ngrok").get_logger()


async def run_ngrok() -> str:
    await setup_ngrok()

    logger.error(">>> Запуск ngrok...")
    ngrok_process = subprocess.Popen(
        ["ngrok", "http", f"{settings.NGROK_PORT}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    time.sleep(5)  # Ожидание запуска ngrok
    if ngrok_process.poll() is not None:
        raise Exception("Ngrok process failed to start")

    logger.error(">>> Получение URL туннеля...")
    for _ in range(5):
        try:
            response = requests.get("http://localhost:4040/api/tunnels")
            if response.status_code == 200:
                break
        except requests.RequestException as e:
            logger.error(f"Ошибка при подключении к ngrok API: {e}")
        time.sleep(2)
    else:
        raise Exception("Ngrok API не отвечает")

    tunnels = response.json().get("tunnels", [])
    if not tunnels:
        raise Exception("No tunnels found")

    public_url = tunnels[0].get("public_url")
    if not public_url:
        raise Exception("No public URL found")

    logger.error(f">>> Туннель ngrok запущен: {public_url}")
    return public_url


async def setup_ngrok() -> None:
    logger.error(">>> Проверка наличия ngrok...")
    ngrok_path = subprocess.run(["which", "ngrok"], capture_output=True, text=True).stdout.strip()
    if not ngrok_path:
        raise Exception("Ngrok is not installed")

    logger.error(">>> Проверка наличия токена аутентификации...")
    if not getattr(settings, 'NGROK_TOKEN', None):
        raise Exception("Ngrok token is not provided")

    config_path = "/root/.config/ngrok/ngrok.yml"

    logger.error(">>> Настройка ngrok...")
    if not os.path.exists(config_path):
        subprocess.run(["ngrok", "config", "add-authtoken", settings.NGROK_TOKEN])
        logger.error(">>> Токен аутентификации добавлен!")
    else:
        logger.error(">>> Токен аутентификации уже добавлен!")
