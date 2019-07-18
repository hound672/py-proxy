import logging
import argparse

logger = logging.getLogger(__name__)


def init_args() -> argparse.Namespace:
    """Init args params"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--log-level', default='INFO',
                        help='Log level: DEBUG, INFO (by default), WARNING, ERROR, CRITICAL')
    parser.add_argument('--host', default='127.0.0.1',
                        help='Host name for listening')
    parser.add_argument('--port', default=8000,
                        help='TCP port for listening')
    return parser.parse_args()


def main() -> None:
    args = init_args()

    log_level = getattr(logging, args.log_level, logging.INFO)
    logging.basicConfig(level=log_level,
                        format='[%(asctime)s]-[%(levelname)s:%(name)s]-[%(filename)s:%(lineno)d]: %(message)s')
    logger.info('Start')


if __name__ == '__main__':
    main()
