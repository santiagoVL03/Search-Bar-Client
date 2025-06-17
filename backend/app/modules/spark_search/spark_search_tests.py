import unittest
import json

from app.modules.spark_search.controller import Spark_searchController


def test_index():
    spark_search_controller = Spark_searchController()
    result = spark_search_controller.index()
    assert result == {'message': 'Hello, World!'}
