import unittest
import json

from app.modules.search.controller import SearchController


def test_index():
    search_controller = SearchController()
    result = search_controller.index()
    assert result == {'message': 'Hello, World!'}
