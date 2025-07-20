#!/usr/bin/env python3
"""Test for client.py"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient class"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that org method returns what get_json returns"""
        mock_get_json.return_value = {"login": org_name}
        client = GithubOrgClient(org_name)
        result = client.org()
        mock_get_json.assert_called_once()
        self.assertEqual(result, mock_get_json.return_value)

if __name__ == "__main__":
    unittest.main()