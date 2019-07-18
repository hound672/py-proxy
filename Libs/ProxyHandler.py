from socketserver import StreamRequestHandler

from Libs.HttpParser import HttpHeader


class ProxyHandler(StreamRequestHandler):
    def handle(self):
        print('--------------')
        incoming_header = HttpHeader.read_from_buffer(self.rfile)
        pass

