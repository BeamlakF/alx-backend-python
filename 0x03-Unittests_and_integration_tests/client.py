#!/usr/bin/env python3
"""Client module."""

import requests


def get_json(url: str):
    """Make an HTTP GET request and return JSON response."""
    response = requests.get(url)
    return response.json()


class GithubOrgClient:
    """Github organization client."""

    def __init__(self, org_name: str):
        self.org_name = org_name

    def org(self):
        """Get organization info from GitHub."""
        url = f"https://api.github.com/orgs/{self.org_name}"
        return get_json(url)
