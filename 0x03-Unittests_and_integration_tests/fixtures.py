#!/usr/bin/env python3
"""Test fixtures"""

org_payload = {
    "login": "testorg",
    "id": 1,
    "url": "https://api.github.com/orgs/testorg",
    "repos_url": "https://api.github.com/orgs/testorg/repos",
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
