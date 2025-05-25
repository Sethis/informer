from dataclasses import dataclass


@dataclass(slots=True, kw_only=True, frozen=True)
class Config:
    db_url: str
    token: str
    redis_host: str
    redis_port: int
    redis_password: str
    redis_db: int
    encoder_offset: int
