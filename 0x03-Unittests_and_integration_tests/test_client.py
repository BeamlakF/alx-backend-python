#!/usr/bin/env python3
"""
Unit tests for client.GithubOrgClient class.
"""

import unittest
from unittest.mock import patch, PropertyMock, MagicMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
import fixtures


class TestGithubOrgClient(unittest.TestCase):
    """
    Test suite for GithubOrgClient.

    This class contains unit tests that verify the functionality
    of the GithubOrgClient methods using mocks.
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """
        Test that the 'org' property returns the expected payload.

        Args:
            org_name (str): The organization name to test.
            mock_get_json (MagicMock): Mocked get_json function.
        """
        test_payload = {"login": org_name, "id": 12345}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, test_payload)

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """
        Test that public_repos returns the expected repository names.

        Args:
            mock_get_json (MagicMock): Mocked get_json function.
        """
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = test_payload

        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = "https://fake.url/api"
            client = GithubOrgClient("testorg")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("https://fake.url/api")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Test that has_license correctly identifies license matches.

        Args:
            repo (dict): Repository dictionary with license info.
            license_key (str): License key to match.
            expected (bool): Expected result of license match.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)

    @patch("client.GithubOrgClient.org", new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """
        Test that _public_repos_url property returns the correct URL.

        Args:
            mock_org (MagicMock): Mocked org property.
        """
        mock_org.return_value = {
            "repos_url": "https://api.github.com/orgs/test_org/repos"
        }
        client = GithubOrgClient("test_org")
        self.assertEqual(
            client._public_repos_url,
            "https://api.github.com/orgs/test_org/repos"
        )


@parameterized_class([
    {
        "org_payload": fixtures.org_payload,
        "repos_payload": fixtures.repos_payload,
        "expected_repos": fixtures.expected_repos,
        "apache2_repos": [repo["name"] for repo in fixtures.apache2_repos],
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for GithubOrgClient.

    Uses actual fixtures and patches requests.get to simulate
    real HTTP calls to GitHub API endpoints.
    """

    @classmethod
    def setUpClass(cls):
        """
        Setup class-wide patcher for requests.get with a side_effect function.

        The side_effect mocks API responses based on the requested URL.
        """
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        def side_effect(url):
            if url == cls.org_payload["url"]:
                return MagicMock(json=lambda: cls.org_payload)
            elif url == cls.org_payload["repos_url"]:
                return MagicMock(json=lambda: cls.repos_payload)
            return MagicMock(json=lambda: None)

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get after all tests are done."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns the expected list of repo names."""
        client = GithubOrgClient(self.org_payload["login"])
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Test public_repos returns the filtered list when license is specified.
        """
        client = GithubOrgClient(self.org_payload["login"])
        self.assertEqual(
            client.public_repos("apache-2.0"),
            self.apache2_repos
        )


if __name__ == "__main__":
    unittest.main()
