#!/usr/bin/env python3
"""Unittests for client.GithubOrgClient._public_repos_url"""

from parameterized import parameterized  # type: ignore
from unittest.mock import patch, PropertyMock
import unittest
from client import GithubOrgClient

class TestGithubOrgClient(unittest.TestCase):

    @parameterized.expand([
        ("google",),
        ("abc",),
        ("alx",),
        ("github",),
        ("holberton",),
        ("microsoft",),
        ("openai",),
        ("apple",),
    ])
    def test_public_repos_url(self, org_name):
        """Test that _public_repos_url returns correct URL from org payload"""
        payload = {"repos_url": f"https://api.github.com/orgs/{org_name}/repos"}
        with patch.object(GithubOrgClient, "org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = payload
            client = GithubOrgClient(org_name)
            self.assertEqual(client._public_repos_url, payload["repos_url"])

if __name__ == "__main__":
    unittest.main()


