from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "voice2text"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"

    MINIO_ROOT_USER: str = "minioadmin"
    MINIO_ROOT_PASSWORD: str = "minioadmin"
    MINIO_BUCKET_NAME: str = "audiofiles"
    
    MINIO_PORT: int = 9000
    MINIO_CONSOLE_PORT: int = 9001
    MINIO_HOST: str = "localhost"
    MINIO_PROTOCOL: str = "http"
    MINIO_ENDPOINT: str = f"{MINIO_PROTOCOL}://{MINIO_HOST}:{MINIO_PORT}"

    # MINIO_ENDPOINT: str = "http://localhost:9000"

    RABBITMQ_HOST: str = "rabbitmq"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_QUEUE: str = "voice_tasks"
    RABBITMQ_USER: str
    RABBITMQ_PASS: str

    LOGGING_CONFIG_FILE: str = "config/logging.conf.yml"

    WHISPER_MODEL: str = "small"
    MODELS_DIR: str = "/models"
    DEVICE_TYPE: str = "cpu"  # Используйте "cuda" для GPU

    TELEGRAM_BOT_TOKEN: str

    BOT_MODE: str = "polling"  # Возможные значения: "polling" или "webhook"

    # NGROK SETTINGS
    NGROK_TOKEN: str
    NGROK_PROTOCOL: str = "http"
    NGROK_PORT: str = "8080"

    WEBHOOK_PORT: int = 8080
    WEBHOOK_PATH: str = "/webhook"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_TTL: int = 3600

    # bot middlewares settings
    MAX_VOICE_DURATION: int = 30
    MAX_VOICE_SIZE: int = 2000000

    @property
    def DATABASE_URL(self):
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:" +
            f"{self.POSTGRES_PASSWORD}@" +
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    class Config:
        env_file = "../.env"  # Укажите правильный путь к файлу .env

settings = Settings()
