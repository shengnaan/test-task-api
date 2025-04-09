import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_SERVER = os.getenv("DB_SERVER")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DATABASE_URL = (f"postgresql+asyncpg://"
                    f"{DB_USER}:{DB_PASSWORD}@{DB_SERVER}:"
                    f"{DB_PORT}/{DB_NAME}")

    API_PORT = os.getenv("API_PORT")
    API_VERSION = os.getenv("API_VERSION")
    API_TITLE = os.getenv("API_TITLE")
    API_DESCRIPTION = os.getenv("API_DESCRIPTION")
    PROJECT_VERSION = os.getenv("PROJECT_VERSION")

    ORIGINS = [
        "*"
    ]
