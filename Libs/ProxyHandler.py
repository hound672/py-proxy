import logging
from socketserver import StreamRequestHandler

from Libs.HttpParser import HttpHeader
from Libs.Request import Request

logger = logging.getLogger(__name__)


class ProxyHandler(StreamRequestHandler):
    def handle(self) -> None:
        header = HttpHeader.read_from_buffer(self.rfile)
        if not header:
            return

        logging.info(f'Request: {header["main"]}')
        request = Request(header)
        data = request.send_request()
        self.wfile.write(data)
