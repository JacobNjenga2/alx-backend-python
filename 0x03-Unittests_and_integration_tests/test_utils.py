#!/usr/bin/env python3
"""Unittests for utils.access_nested_map function"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import access_nested_map
import unittest
from parameterized import parameterized # type: ignore

class TestAccessNestedMap(unittest.TestCase):
    """Test cases for the access_nested_map utility function"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Test that access_nested_map returns expected result for various inputs
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

        @parameterized.expand([
            ({}, ("a",), 'a'),
            ({"a": 1}, ("a", "b"), 'b'),

        ])
        def test_access_nested_map_exception(self, nested_map, path, expected_key):
            """Test that KeyError is raised with correct message"""
            with self.assertRaises(KeyError) as cm:
                access_nested_map(nested_map, path)
            self.assertEqual(str(cm.exception), repr(expected_key))

if __name__ == '__main__':
    unittest.main()
