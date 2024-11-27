import os

DATABASE_NAME = os.getenv("DATABASE_NAME", "homework")
DATABASE_USER = os.getenv("DATABASE_USER", "user")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "random")
DATABASE_HOST = os.getenv("DATABASE_HOST", "store")
DATABASE_PORT = os.getenv("DATABASE_PORT", "5432")

DATABASE_URL = f"postgres://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"


TORTOISE_ORM = {
    "connections": {
        "default": DATABASE_URL  # Замените на ваши параметры подключения
    },
    "apps": {
        "models": {
            "models": ["enterprise.models"],  # Замените на свои модели
            "default_connection": "default",
        },
    },
}