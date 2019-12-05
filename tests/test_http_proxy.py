# -*- coding: utf-8 -*-

"""Test http_proxy."""

from unittest.mock import Mock, patch, create_autospec

import pytest

from py_proxy.http_proxy import HttpProxy


@patch('py_proxy.http_proxy.HttpParser')
def test_connection_made(mock_http_parser):
    """Test for connection made."""
    http_proxy = HttpProxy()
    mock_transport = Mock()

    http_proxy.connection_made(mock_transport)

    mock_http_parser.assert_called_with()
    assert http_proxy._transport == mock_transport
    assert http_proxy._request_parser == mock_http_parser.return_value


def test_data_received():
    """Test for data received."""
    http_proxy = HttpProxy()
    http_proxy._request_parser = Mock()
    mock_received_data = Mock()

    http_proxy.data_received(mock_received_data)
    http_proxy._request_parser.feed_data.assert_called_with(mock_received_data)
