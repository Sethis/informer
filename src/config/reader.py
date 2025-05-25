import os

from dotenv import load_dotenv

load_dotenv("env.env")

from .structure import Config

def reader() -> Config:
    return Config(
        db_url=os.getenv("DB_URL"),
        token=os.getenv("TOKEN"),
        redis_host=os.getenv("REDIS_HOST"),
        redis_port=int(os.getenv("REDIS_PORT")),
        redis_password=os.getenv("REDIS_PASSWORD"),
        redis_db=int(os.getenv("REDIS_DB")),
        encoder_offset=int(os.getenv("ENCODER_OFFSET"))
    )
