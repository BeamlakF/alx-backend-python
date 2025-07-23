#!/usr/bin/env python3
"""
Unit tests for client.GithubOrgClient class.
"""

import unittest
from unittest.mock import patch, PropertyMock, MagicMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient methods"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test GithubOrgClient.org returns correct value"""
        test_payload = {"name": org_name}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, test_payload)
        mock_get_json.assert_called_once_with(
            GithubOrgClient.ORG_URL.format(org=org_name)
        )

    def test_public_repos_url(self):
        """Test GithubOrgClient._public_repos_url returns correct URL"""
        with patch("client.GithubOrgClient.org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "https://api.github.com/orgs/test_org/repos"}
            client = GithubOrgClient("test_org")
            self.assertEqual(client._public_repos_url, "https://api.github.com/orgs/test_org/repos")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos returns list of repo names"""
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"}
        ]
        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/test_org/repos"
            client = GithubOrgClient("test_org")
            result = client.public_repos()
            self.assertEqual(result, ["repo1", "repo2"])

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test GithubOrgClient.has_license correctly evaluates license"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": [repo["name"] for repo in apache2_repos],
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient with fixtures"""

    @classmethod
    def setUpClass(cls):
        """Set up mocks before running tests"""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        def side_effect(url):
            if url == GithubOrgClient.ORG_URL.format(org=cls.org_payload["login"]):
                return MagicMock(json=lambda: cls.org_payload)
            elif url == cls.org_payload["repos_url"]:
                return MagicMock(json=lambda: cls.repos_payload)
            return MagicMock(json=lambda: None)

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher after all tests"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repos"""
        client = GithubOrgClient(self.org_payload["login"])
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos with license filter"""
        client = GithubOrgClient(self.org_payload["login"])
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)
