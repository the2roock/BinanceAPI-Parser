import os


class DatabaseConfig:
    # mysql
    host = os.getenv("DATABASE_HOST")
    user = os.getenv("DATABASE_USER")
    port = os.getenv("DATABASE_PORT")
    password = os.getenv("DATABASE_PASSWORD")
    name = os.getenv("DATABASE_NAME")
