import logging
from logging.handlers import RotatingFileHandler

# Настройка уровня логирования и конфигурация логгера
logging.basicConfig(level=logging.INFO, filemode='w')
logger = logging.getLogger(__name__)
# Добавление обработчика для файла
file_handler = RotatingFileHandler('app.log', backupCount=1)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)