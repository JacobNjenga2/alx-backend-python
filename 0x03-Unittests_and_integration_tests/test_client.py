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
        """
        Test that GithubOrgClient.org returns expected data
        and calls get_json with the correct URL.
        """
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
        """
        Test that _public_repos_url returns the correct repos_url
        based on the mocked org property (which is memoized).
        """
        expected_url = f"https://api.github.com/orgs/{org_name}/repos"
        payload = {"repos_url": expected_url}

        # Patch the memoized org property to return the payload
        with patch.object(GithubOrgClient, "org", new_callable=property) as mock_org:
            mock_org.return_value = payload
            client = GithubOrgClient(org_name)
            self.assertEqual(client._public_repos_url, expected_url)


if __name__ == "__main__":
    unittest.main()

