#!/usr/bin/env python3
"""Unittests for client.GithubOrgClient"""

import unittest
from unittest.mock import patch
from parameterized import parameterized  # type: ignore
from client import GithubOrgClient

class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient"""

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
    def test_org(self, org_name):
        """Test that GithubOrgClient.org returns expected data and calls get_json"""
        payload = {"login": org_name}
        with patch('client.get_json') as mock_get_json:
            mock_get_json.return_value = payload
            client = GithubOrgClient(org_name)
            self.assertEqual(client.org, payload)
            mock_get_json.assert_called_once_with(
                f"https://api.github.com/orgs/{org_name}"
            )

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
        with patch.object(GithubOrgClient, "org", new_callable=property) as mock_org:
            mock_org.return_value = payload
            client = GithubOrgClient(org_name)
            self.assertEqual(client._public_repos_url, payload["repos_url"])

if __name__ == "__main__":
    unittest.main()

