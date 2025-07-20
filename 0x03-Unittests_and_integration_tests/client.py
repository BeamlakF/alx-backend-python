#!/usr/bin/env python3
"""Client module."""

from utils import get_json  


class GithubOrgClient:
    """GitHub organization client."""

    def __init__(self, org_name):
        self.org_name = org_name

    def org(self):
        """Return organization info."""
        url = f"https://api.github.com/orgs/{self.org_name}"
        return get_json(url)
