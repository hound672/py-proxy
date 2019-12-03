# -*- coding: utf-8 -*-

"""Fixtures."""

import socket

import pytest


@pytest.fixture
def get_unused_port():
    """Return unsed port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('127.0.0.1', 0))
        return sock.getsockname()[1]
