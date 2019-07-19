import socket
from dataclasses import dataclass
from urllib.parse import urlparse
from typing import Any


@dataclass
class Settings:
    log_level: str = 'INFO'
    host: str = 'localhost'
    port: int = 9001
    # target_url: str = 'https://habr.com'
    # target_url: str = 'https://www.f1-world.ru'
    target_url: str = 'https://stackoverflow.com'

    @property
    def local_url(self) -> str:
        """Return local link"""
        return f'http://{self.host}:{self.port}'

    @property
    def target_host(self) -> str:
        """Return target hostname"""
        url = urlparse(self.target_url)
        return url.netloc

    @property
    def target_port(self) -> int:
        """Return target port"""
        url = urlparse(self.target_url)
        scheme = url.scheme
        return 443 if scheme == 'https' else 22

    def set_target_url(self, url: Any) -> None:
        """Set target url after redirect maybe"""
        # TODO not so good solutions
        self.target_url = f'{url.scheme}://{url.netloc}'


settings = Settings()
