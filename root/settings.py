import os

from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "engine": os.getenv("DB_ENGINE"),
    "name": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}
