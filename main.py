import logging
import argparse
from socketserver import TCPServer

from Libs.ProxyHandler import ProxyHandler

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """Init args params"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--log-level', default='INFO',
                        help='Log level: DEBUG, INFO (by default), WARNING, ERROR, CRITICAL')
    parser.add_argument('--host', default='localhost',
                        help='Host name for listening')
    parser.add_argument('--port', default=9001,
                        help='TCP port for listening')
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    log_level = getattr(logging, args.log_level, logging.INFO)
    logging.basicConfig(level=log_level,
                        format='[%(asctime)s]-[%(levelname)s:%(name)s]-[%(filename)s:%(lineno)d]: %(message)s')

    logger.info(f'Start server: {args.host}:{args.port}')

    server = TCPServer((args.host, args.port), ProxyHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info('Exit...')
        server.server_close()


if __name__ == '__main__':
    main()
