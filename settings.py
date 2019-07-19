from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass
class Settings:
    log_level: str = 'INFO'
    host: str = 'localhost'
    port: int = 9001
    # target_url: str = 'https://habr.com'
    target_url: str = 'http://habrahabr.ru'

    @property
    def local_url(self):
        """Return local link"""
        return f'http://{self.host}:{self.port}'

    def set_target_url(self, url: 'urlparse'):
        """Set target url after redirect maybe"""
        # TODO not so goog solutions
        self.target_url = f'{url.scheme}://{url.netloc}'


settings = Settings()
