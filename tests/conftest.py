# -*- coding: utf-8 -*-

"""Fixtures."""

import socket
import pathlib
from typing import NamedTuple

import pytest
from faker import Factory


class ServerAddress(NamedTuple):
    """Tuple for server address."""

    host: str
    port: int


@pytest.fixture
def get_server_address():
    """Return unsed port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('127.0.0.1', 0))
        port = sock.getsockname()[1]
    host = 'localhost'

    return ServerAddress(host, port)


@pytest.fixture
def faker():
    """Create faker object."""
    return Factory.create()


@pytest.fixture
def files_dir():
    """Return dir to files for tests."""
    return pathlib.Path(__file__).parent / 'files'
