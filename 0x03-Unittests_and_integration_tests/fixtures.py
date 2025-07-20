#!/usr/bin/env python3
"""Fixtures for unit and integration tests."""

org_payload = {
    "login": "test_org",
    "id": 1,
    "url": "https://api.github.com/orgs/test_org",
    "repos_url": "https://api.github.com/orgs/test_org/repos"
}

repos_payload = [
    {"id": 101, "name": "repo1", "license": {"key": "apache-2.0"}},
    {"id": 102, "name": "repo2", "license": {"key": "mit"}},
    {"id": 103, "name": "repo3", "license": {"key": "apache-2.0"}},
]

expected_repos = ["repo1", "repo2", "repo3"]

apache2_repos = [
    {"id": 101, "name": "repo1", "license": {"key": "apache-2.0"}},
    {"id": 103, "name": "repo3", "license": {"key": "apache-2.0"}},
]
