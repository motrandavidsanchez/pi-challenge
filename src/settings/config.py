import os

from starlette.config import Config

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
__config = Config(os.path.join(os.path.dirname(ROOT_DIR), ".env"))

# General
IS_DEBUG: bool = __config("IS_DEBUG", cast=bool, default=False)
SECRET_KEY: str = __config("SECRET_KEY", cast=str, default="CHANGE_ME!!!")

# Project
APP_DESCRIPTION: str = __config("APP_DESCRIPTION", cast=str, default="")
APP_NAME: str = __config("APP_NAME", cast=str, default="")
APP_VERSION: str = __config("APP_VERSION", cast=str, default="0.0.1")
DOCS_URL: str = "/docs" if IS_DEBUG else None

# Database
DATABASE_URL: str = __config("DATABASE_URL", cast=str)
