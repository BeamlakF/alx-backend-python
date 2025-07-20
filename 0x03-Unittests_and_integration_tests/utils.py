#!/usr/bin/env python3
"""Utils module."""

from typing import Mapping, Any, Sequence, Union, Callable
import requests
from functools import wraps


def access_nested_map(nested_map: Mapping, path: Sequence) -> Union[Any, None]:
    """
    Access value in a nested map with a given path.

    Args:
        nested_map (Mapping): The nested mapping to traverse.
        path (Sequence): Sequence of keys to traverse the nested_map.

    Returns:
        The value found at the nested path.

    Raises:
        KeyError: If any key in the path does not exist or path is invalid.
    """
    current = nested_map
    for key in path:
        if not isinstance(current, Mapping):
            raise KeyError(key)
        if key not in current:
            raise KeyError(key)
        current = current[key]
    return current


def get_json(url: str) -> Any:
    """
    Fetch JSON content from a given URL.

    Args:
        url (str): The URL to make the GET request to.

    Returns:
        The JSON response parsed to Python data.
    """
    response = requests.get(url)
    return response.json()


def memoize(fn: Callable) -> Callable:
    """
    Decorator to cache the result of a method call.

    Args:
        fn (Callable): The method to memoize.

    Returns:
        Callable: The memoized property.
    """
    attr_name = "_memoized_" + fn.__name__

    @property
    @wraps(fn)
    def memoized(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    return memoized
