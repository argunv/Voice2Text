import logging

logger = logging.getLogger("error_handler")

def log_exception(exception: Exception, context: str = "General"):
    """
    Логирует исключения с указанием контекста.
    """
    logger.error(f"Exception in {context}: {str(exception)}", exc_info=True)
