from dataclasses import dataclass


@dataclass
class Settings:
    log_level: str = 'INFO'
    host: str = 'localhost'
    port: int = 9001


settings = Settings()
