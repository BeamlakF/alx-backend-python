#!/usr/bin/env python3
"""
Fixtures for testing GithubOrgClient.
"""

org_payload = {
    "login": "test_org",
    "id": 123456,
    "url": "https://api.github.com/orgs/test_org",
    "repos_url": "https://api.github.com/orgs/test_org/repos"
}

repos_payload = [
    {"name": "repo1", "license": {"key": "apache-2.0"}},
    {"name": "repo2", "license": {"key": "mit"}},
    {"name": "repo3", "license": {"key": "apache-2.0"}},
]

expected_repos = ["repo1", "repo2", "repo3"]

apache2_repos = [
    {"name": "repo1", "license": {"key": "apache-2.0"}},
    {"name": "repo3", "license": {"key": "apache-2.0"}},
]
