#!/usr/bin/env python3
"""Utils module."""

from typing import Mapping, Any, Sequence, Union

def access_nested_map(nested_map: Mapping, path: Sequence) -> Union[Any, None]:
    """Access value in a nested map with a given path."""
    for key in path:
        nested_map = nested_map[key]
    return nested_map
