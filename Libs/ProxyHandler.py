import logging
import ssl
import socket
from typing import BinaryIO
from socketserver import StreamRequestHandler
from contextlib import AbstractContextManager

from settings import settings
from Libs.HttpParser import HttpHeader
from Libs.Request import Request
from Libs.Response import Response

logger = logging.getLogger(__name__)


class SocketContextManager(AbstractContextManager):
    """Context manager for read from socket"""

    def __enter__(self) -> BinaryIO:
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket = ssl.wrap_socket(self._socket, ssl_version=ssl.PROTOCOL_TLSv1)
        self._socket.connect((settings.target_host, settings.target_port))  # TODO from settings
        self._file = self._socket.makefile('rwb')
        return self._file

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self._file.close()
        self._socket.close()


########################################################

class ProxyHandler(StreamRequestHandler):
    def handle(self) -> None:
        """Handler for incoming request"""
        header_request = HttpHeader.read_from_buffer(self.rfile)
        if not header_request:
            return

        request = Request(header_request)
        logger.info(f'Request: {request.path}')

        response = self.send_request(request)
        logger.info(f'Response: {response.path}')

        for chunk in response:
            self.wfile.write(chunk)

    def send_request(self, request: Request) -> Response:
        """Send request to host. And read response"""

        with SocketContextManager() as file:
            file.write(bytes(request))
            file.flush()
            response = self.read_response(file)

        return response

    def read_response(self, buffer: BinaryIO) -> Response:
        """Read response from host"""

        # first read header
        header_response = HttpHeader.read_from_buffer(buffer)

        data = bytearray() # TODO TEMP !!!
        # read content
        if 'Transfer-Encoding' in header_response and header_response['Transfer-Encoding'].lower() == 'chunked':
            logger.debug('There is chunked data')
            data = self._read_response_chunks(buffer)
        elif 'Content-Length' in header_response:
            logger.info('There is Content-Length')
            data = self._read_response_full(header_response, buffer)

        return Response(header_response, data)

    ########################################################

    def _read_response_chunks(self, buffer: BinaryIO) -> bytearray:
        """Read response content by chunks"""
        chunk_size = self._get_chunk_size(buffer)
        content = bytearray()
        while chunk_size:
            logger.debug(f'Chunk size: {chunk_size}')

            read = buffer.read(chunk_size)
            content.extend(read)

            chunk_size = self._get_chunk_size(buffer)

        logger.debug(f'Total content size: {len(content)}')
        return content

    @staticmethod
    def _get_chunk_size(buffer: BinaryIO) -> int:
        """Return chunk's size"""
        data = buffer.readline()
        if data == b'\r\n':
            data = buffer.readline()
        size = int(data.strip(), 16)
        return size

    ########################################################

    def _read_response_full(self, header: HttpHeader, buffer: BinaryIO) -> bytearray:
        """Read full response """
        content_size = int(header['Content-Length'])
        data = buffer.read(content_size)
        return bytearray(data)
