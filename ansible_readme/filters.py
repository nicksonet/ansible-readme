"""Jinja2 filters module."""

import typing


def listify(value: typing.Union[typing.List, str]) -> str:
    """Turn a list of items into a Markdown formatted list."""
    linked = []
    if isinstance(value, list):
        for default in value:
            linked.append(f'  * ``{default}``')
        return '\n{}'.format('\n'.join(linked))
    return f'``{value}``'


def quicklistify(value: typing.Dict[str, typing.Any]) -> str:
    """Inline Markdown link a list of defaults."""
    linked = []
    for default in value:
        linked.append(f'[{default}](#{default})')
    return ', '.join(linked)
