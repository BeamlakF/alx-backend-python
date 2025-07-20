#!/usr/bin/env python3
"""Client module."""

import requests


def get_json(url):
    """Make an HTTP GET request and return the JSON result."""
    response = requests.get(url)
    return response.json()


class GithubOrgClient:
    """GitHub organization client."""

    def __init__(self, org_name):
        self.org_name = org_name

    def org(self):
        """Return organization info."""
        url = f"https://api.github.com/orgs/{self.org_name}"
        return get_json(url)
