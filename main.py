import logging
import argparse
from socketserver import TCPServer

from settings import settings
from Libs.ProxyHandler import ProxyHandler

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """Init args params"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--log-level', default=settings.log_level,
                        help='Log level: DEBUG, INFO (by default), WARNING, ERROR, CRITICAL')
    parser.add_argument('--host', default=settings.host,
                        help='Host name for listening')
    parser.add_argument('--port', default=9001, type=int,
                        help='TCP port for listening')
    args = parser.parse_args()
    settings.log_level = args.log_level
    settings.host = args.host
    settings.port = args.port
    return args


def main() -> None:
    args = parse_args()
    print(f'Settings: {settings}')

    log_level = getattr(logging, args.log_level, logging.INFO)
    logging.basicConfig(level=log_level,
                        format='[%(asctime)s]-[%(levelname)s:%(name)s]-[%(filename)s:%(lineno)d]: %(message)s')

    logger.info(f'Start server: {settings.host}:{settings.port}')

    server = TCPServer((settings.host, settings.port), ProxyHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info('Exit...')
        server.server_close()


if __name__ == '__main__':
    main()
