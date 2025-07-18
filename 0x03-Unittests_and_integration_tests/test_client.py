#!/usr/bin/env python3
"""Unittests for client.GithubOrgClient"""

from parameterized import parameterized
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

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns expected repo names and mocks are called once"""
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = test_payload
        test_url = "https://api.github.com/orgs/testorg/repos"

        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = test_url
            client = GithubOrgClient("testorg")
            repos = client.public_repos()
            self.assertEqual(repos, ["repo1", "repo2", "repo3"])
            mock_get_json.assert_called_once_with(test_url)
            mock_url.assert_called_once()

if __name__ == "__main__":
    unittest.main()
