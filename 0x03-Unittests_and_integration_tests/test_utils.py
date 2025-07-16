#!/usr/bin/env python3
"""Unittests for utils.access_nested_map function"""

import unittest
from parameterized import parameterized # type: ignore
from utils import access_nested_map

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

if __name__ == '__main__':
    unittest.main()
