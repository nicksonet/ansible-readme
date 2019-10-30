"""The AnsibleReadme core module.

All documentation context is stored within the AnsibleReadme object along with
any file system locations, configurations and other information relevant to
aiding in documenting roles.
"""

import os
import pathlib
import typing

import attr
import click
import yaml
from jinja2 import Environment, FileSystemLoader

from ansible_readme.filters import listify, quicklistify
from ansible_readme.logger import get_logger, red_text

log = get_logger(__name__)


@attr.s(auto_attribs=True)
class AnsibleReadme:
    """Role documentation and context."""

    # Initial path to look for Ansible roles in
    path: pathlib.Path = attr.ib()

    # If self.path points to a directory which has one Ansible roles
    is_single_role: bool = attr.ib(default=False)

    # If self.path points to a directory which has several Ansible roles
    is_multiple_role: bool = attr.ib(default=False)

    # All paths discovered which hold an Ansible role
    role_paths: typing.List[pathlib.Path] = attr.ib(default=attr.Factory(list))

    # Documentation gathered about roles to be placed in README files
    role_docs: typing.Dict[str, typing.Any] = attr.ib(
        default=attr.Factory(dict)
    )

    # Rendered readme files generated and populated with self.role_docs
    role_readmes: typing.Dict[str, str] = attr.ib(default=attr.Factory(dict))

    # Conventional Ansible role paths to help identify roles programmatically
    STANDARD_ROLE_PATHS: typing.List[str] = [
        'defaults',
        'files',
        'meta',
        'molecule',
        'tasks',
        'templates',
        'vars',
    ]

    # Whether or not to overwrite a REAMDE file on disk
    should_force: bool = attr.ib(default=False)

    # Jinaj2 template to use for README generation
    template: pathlib.Path = attr.ib(
        default=pathlib.Path(__file__).parent.absolute()
        / 'data'
        / 'readme.md.j2'
    )

    # Default generated README file name
    readme_name: str = attr.ib(default='README.md')

    # Whether or not to output debugging information
    debug: bool = attr.ib(default=False)

    # Click based command line context
    context: typing.Any = attr.ib(default=None)

    def __attrs_post_init__(self):
        """Initalise state after validation has run through."""
        self.path = pathlib.Path(self.path).absolute()
        self.role_paths = self.gather_role_paths()

        if self.debug:
            paths = ', '.join(map(str, self.role_paths))
            log.info('Role paths are {}'.format(paths))

    @path.validator
    def __check_path(
        self, attribute: attr.Attribute, value: pathlib.Path
    ) -> typing.Optional[Exception]:
        """Ensure 'value' does indeed contain a role or roles."""
        path = pathlib.Path(value).absolute()

        if self.is_role_path(path) or self.is_roles_path(path):
            if self.debug:
                msg = (
                    'a single role' if self.is_single_role else 'multiple roles'
                )
                log.info(f'{path} contains {msg}')
            return None

        raise click.ClickException(
            red_text(f'{path} does not contain any Ansible roles?')
        )

    def has_standard_role_paths(self, path: pathlib.Path) -> bool:
        """Does 'path' contain standard role paths?"""
        _dirs = [
            _dir for _dir in os.listdir(path) if os.path.isdir(path / _dir)
        ]

        if not any(_dir in self.STANDARD_ROLE_PATHS for _dir in _dirs):
            return False

        main_yml_paths = [
            path / _dir / 'main.yml' for _dir in self.STANDARD_ROLE_PATHS
        ]

        if not any(os.path.exists(main_yml) for main_yml in main_yml_paths):
            return False

        return True

    def is_role_path(self, path: pathlib.Path) -> bool:
        """Does 'path' contain a role?"""
        if self.has_standard_role_paths(path):
            self.is_single_role = True
        else:
            self.is_single_role = False

        return self.is_single_role

    def is_roles_path(self, path: pathlib.Path) -> bool:
        """Does 'path' contain at least one role?"""
        if self.is_single_role:
            self.is_multiple_role = False
            return self.is_multiple_role

        _dirs = [
            path / _dir
            for _dir in os.listdir(path)
            if os.path.isdir(path / _dir)
        ]

        for _dir in _dirs:
            if self.has_standard_role_paths(_dir):
                self.is_multiple_role = True

        return self.is_multiple_role

    def gather_role_paths(self) -> typing.List[pathlib.Path]:
        """Retrieve a list of valid role paths after validation."""
        if self.is_single_role:
            return [self.path]

        return [
            pathlib.Path(self.path / role_path)
            for role_path in os.listdir(self.path)
            if os.path.isdir(self.path / role_path)
        ]

    def do_gathering(self, path: pathlib.Path) -> typing.Dict[str, typing.Any]:
        """Do actual gathering of information specifed at path."""
        contents: typing.Dict[str, typing.Any] = {}

        if os.path.exists(path):
            with open(path) as file:
                loaded = yaml.load(file.read(), Loader=yaml.SafeLoader)
                contents = loaded if loaded else {}

        return contents

    def gather_meta(self, path: pathlib.Path) -> typing.Dict[str, typing.Any]:
        """Gather all meta for a role."""
        contents = self.do_gathering(path / 'meta' / 'main.yml')

        if 'galaxy_info' not in contents:
            contents['galaxy_info'] = {}

        return contents

    def gather_docs(self, path: pathlib.Path) -> typing.Dict[str, typing.Any]:
        """Gather docs/ path documentation for a role."""
        return self.do_gathering(path / 'docs' / 'main.yml')

    def gather_defaults(
        self, path: pathlib.Path
    ) -> typing.Dict[str, typing.Any]:
        """Gather all defaults for a role."""
        return self.do_gathering(path / 'defaults' / 'main.yml')

    def gather_extras(self, path: pathlib.Path) -> typing.Dict[str, typing.Any]:
        """Gather extra context documentation for a role."""
        contents: typing.Dict[str, typing.Any] = {}
        contents['role_name'] = os.path.basename(path)
        return contents

    def gather_all(self) -> typing.Dict[str, typing.Any]:
        """Gather all documentation for roles."""
        for path in self.role_paths:
            role_name = os.path.basename(path)
            self.role_docs[role_name] = {
                'meta': self.gather_meta(path),
                'defaults': self.gather_defaults(path),
                'extras': self.gather_extras(path),
                'docs': self.gather_docs(path),
            }

        if self.debug:
            log.info(f'Gathered role documentation: {self.role_docs}')

        return self.role_docs

    def render_readmes(self) -> typing.Dict[str, str]:
        """Render README file templates using Jinja2 with gathered docs."""
        template_path = str(pathlib.Path(self.template).parent.absolute())

        jinja_env = Environment(
            loader=FileSystemLoader(template_path),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        jinja_env.filters['listify'] = listify
        jinja_env.filters['quicklistify'] = quicklistify

        template = jinja_env.get_template(os.path.basename(self.template))

        for role_doc in self.role_docs:
            self.role_readmes[role_doc] = template.render(
                **self.role_docs[role_doc]
            )

        return self.role_readmes

    def write_readmes(self) -> None:
        """Write README files from rendered templates."""
        for path in self.role_paths:
            role_name = os.path.basename(path)
            readme_path = path / self.readme_name

            if self.debug:
                log.info(
                    'README will look like:\n\n{}'.format(
                        self.role_readmes[role_name]
                    )
                )

            if os.path.exists(readme_path) and not self.should_force:
                msg = (
                    'Discovered {} which already exists, refusing '
                    'to overwrite (pass --force to override this)'
                ).format(readme_path)
                raise click.ClickException(red_text(msg))

            with open(readme_path, 'w') as readme_handle:
                readme_handle.write(self.role_readmes[role_name])

    def generate_readmes(self) -> None:
        """Generate READMEs for discovered roles."""
        self.init_docs()
        self.gather_all()
        self.render_readmes()
        self.write_readmes()

    def init_docs(self) -> None:
        """Generate docs/ folders with defaults."""
        for role_path in self.role_paths:
            docs: typing.Dict[str, typing.Any] = {'defaults': {}}
            docs_path = role_path / 'docs'

            is_init_without_force = (
                self.context.command.name == 'init'
                and os.path.exists(docs_path)
                and not self.should_force
            )

            another_cmd = (
                self.context.command.name != 'init'
                and os.path.exists(docs_path)
            )

            if is_init_without_force or another_cmd:
                log.info(
                    f'{docs_path} already exists, skipping '
                    '(use init command with --force to override)'
                )
                continue

            if not os.path.exists(docs_path):
                os.mkdir(docs_path)

            defaults = self.gather_defaults(role_path)
            for default in defaults:
                docs['defaults'].update({default: {'help': 'TODO.'}})

            with open(docs_path / 'main.yml', 'w') as docs_file:
                yaml.dump(
                    docs,
                    docs_file,
                    explicit_start=True,
                    default_flow_style=False,
                )

        return None
