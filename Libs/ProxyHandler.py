import logging
from socketserver import StreamRequestHandler

from Libs.HttpParser import HttpHeader
from Libs.Request import Request

logger = logging.getLogger(__name__)


class ProxyHandler(StreamRequestHandler):
    def handle(self) -> None:
        incoming_header = HttpHeader.read_from_buffer(self.rfile)
        if not incoming_header:
            return

        logging.info(f'Request: {incoming_header["main"]}')
        request = Request(incoming_header)
        request.send_request()
