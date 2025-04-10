import os

from dotenv import load_dotenv

load_dotenv()
load_dotenv(".env.ci")

class Settings:
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_SERVER = os.getenv("DB_SERVER")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_ALEMBIC_SERVER = os.getenv("DB_ALEMBIC_SERVER")
    DATABASE_URL = (f"postgresql+asyncpg://"
                    f"{DB_USER}:{DB_PASSWORD}@{DB_SERVER}:"
                    f"{DB_PORT}/{DB_NAME}")

    DATABASE_URL_ALEMBIC = (f"postgresql+asyncpg://"
                    f"{DB_USER}:{DB_PASSWORD}@{DB_ALEMBIC_SERVER}:"
                    f"{DB_PORT}/{DB_NAME}")

    TEST_POSTGRES_USER = os.getenv("TEST_POSTGRES_USER")
    TEST_POSTGRES_PASSWORD = os.getenv("TEST_POSTGRES_PASSWORD")
    TEST_POSTGRES_SERVER = os.getenv("TEST_POSTGRES_SERVER")
    TEST_POSTGRES_PORT = os.getenv("TEST_POSTGRES_PORT")
    TEST_POSTGRES_DB = os.getenv("TEST_POSTGRES_DB")
    TEST_DATABASE_URL = (f"postgresql+asyncpg://"
                         f"{TEST_POSTGRES_USER}:{TEST_POSTGRES_PASSWORD}@"
                         f"{TEST_POSTGRES_SERVER}:{TEST_POSTGRES_PORT}/"
                         f"{TEST_POSTGRES_DB}")

    API_PORT = os.getenv("API_PORT")
    API_VERSION = os.getenv("API_VERSION")
    API_TITLE = os.getenv("API_TITLE")
    API_DESCRIPTION = os.getenv("API_DESCRIPTION")
    PROJECT_VERSION = os.getenv("PROJECT_VERSION")

    ORIGINS = [
        "*"
    ]
