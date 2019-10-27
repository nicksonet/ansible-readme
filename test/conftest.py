"""Pytest fixtures."""

import pathlib
import typing

import pytest


def __generate_roles(
    role_names: typing.List[str], tmp_path: pathlib.Path
) -> None:
    """Generate dummy roles for testing."""
    STANDARD_ROLE_PATHS = [
        'defaults',
        'files',
        'meta',
        'tasks',
        'templates',
        'vars',
    ]

    for role in role_names:
        role_root = tmp_path / role
        role_root.mkdir()

        for path in STANDARD_ROLE_PATHS:
            role_path = role_root / path
            role_path.mkdir()

            main_yml = role_path / 'main.yml'
            main_yml.write_text('---')

    return None


@pytest.fixture()
def single_role_path(tmp_path):
    __generate_roles(['role1'], tmp_path)
    return tmp_path / 'role1'


@pytest.fixture()
def many_roles_path(tmp_path):
    __generate_roles(['role1', 'role2', 'role3'], tmp_path)
    return tmp_path
