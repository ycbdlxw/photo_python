import os
import pathlib

BACKEND_PATH = pathlib.Path(__file__).parent.parent

SUPER_USER = 1


class Config:
    LOGGING_FILE_D = os.path.dirname(os.path.dirname(__file__))
    LOGGING_FILE_DIR = os.path.join(LOGGING_FILE_D)
    LOGGING_FILE_NAME = 'log.log'
    LOGGING_FILE_PATH = os.path.join(LOGGING_FILE_DIR, LOGGING_FILE_NAME)
    LOGGING_LEVEL = 'INFO'
    # LOGGING_FORMAT = '{time} [{level}] {message}'
    LOGGING_FORMAT = "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"


settings = Config()