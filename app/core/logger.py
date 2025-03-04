import logging
import logging.config
import yaml
import inspect
import os
from config.settings import settings


class Logger:
    def __init__(self, module_name: str = None, config_path: str = None):
        # Создание необходимой папки logs
        os.makedirs("logs", exist_ok=True)

        # Загружаем конфигурацию из файла
        if not config_path:
            if not getattr(settings, 'LOGGING_CONFIG_FILE', None):
                raise ValueError("Не указан путь к файлу конфигурации логирования.")
            config_path = settings.LOGGING_CONFIG_FILE
        try:
            with open(config_path, "r") as f:
                logging_config = yaml.safe_load(f)
            logging.config.dictConfig(logging_config)
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл конфигурации логирования {config_path} не найден.")

        # Получаем имя модуля, который вызвал логгер
        self.module_name = module_name or self._get_caller_module_name()

    def _get_caller_module_name(self):
        """Получает имя модуля, вызвавшего Logger."""
        try:
            return inspect.stack()[1].filename[:-3].split("/")[-1]
        except IndexError:
            return "root"

    def get_logger(self):
        """Возвращает объект логгера."""
        return logging.getLogger(self.module_name)
