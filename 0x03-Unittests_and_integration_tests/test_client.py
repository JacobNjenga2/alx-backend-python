#!/usr/bin/env python3
"""Unittests for client.GithubOrgClient"""

from parameterized import parameterized
from unittest.mock import patch, PropertyMock
import unittest

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unittests for GithubOrgClient methods"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns expected data and calls get_json"""
        test_payload = {"login": org_name, "id": 1}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, test_payload)
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
        """
        Test that _public_repos_url returns correct URL from mocked org property
        """
        payload = {
            "repos_url": (
                f"https://api.github.com/orgs/{org_name}/repos"
            )
        }
        with patch.object(
            GithubOrgClient, "org", new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = payload
            client = GithubOrgClient(org_name)
            self.assertEqual(
                client._public_repos_url,
                payload["repos_url"]
            )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """
        Test that public_repos returns expected repo names and mocks are called once
        """
        payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = payload

        test_url = "https://api.github.com/orgs/test_org/repos"
        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = test_url
            client = GithubOrgClient("test_org")
            result = client.public_repos()
            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(test_url)


if __name__ == "__main__":
    unittest.main()

