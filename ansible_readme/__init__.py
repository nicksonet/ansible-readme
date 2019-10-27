"""CLI entrypoint module."""

__all__ = ['AnsibleReadme']

import pathlib

import click
import colorama

from ansible_readme.__version__ import __version__
from ansible_readme.ansible_readme import AnsibleReadme
from ansible_readme.logger import should_do_markup

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

colorama.init(autoreset=True, strip=not should_do_markup())


@click.group()
@click.version_option(version=__version__)
@click.option(
    '--debug/--no-debug',
    help='Show debug logging',
    default=False,
    show_default=True,
)
@click.pass_context
def __main__(ctx, debug):
    """
    \b
            ___    _   _______ ________  __    ______
           /   |  / | / / ___//  _/ __ )/ /   / ____/
          / /| | /  |/ /\__ \ / // __  / /   / __/
         / ___ |/ /|  /___/ _/ // /_/ / /___/ /___
        /_/ _____/_________/______________________
           / __ \/ ____/   |  / __ \/  |/  / ____/
          / /_/ / __/ / /| | / / / / /|_/ / __/
         / _, _/ /___/ ___ |/ /_/ / /  / / /___
        /_/ |_/_____/_/  |_/_____/_/  /_/_____/

    Generate documenting README files for Ansible roles

    """  # noqa
    ctx.obj = {}
    ctx.obj['debug'] = debug


@__main__.command(context_settings=CONTEXT_SETTINGS)
@click.argument(
    'roles-path', type=click.Path(exists=True), default=pathlib.Path('.')
)
@click.pass_context
@click.option(
    '--force/--no-force',
    help='Overwrite existing docs/ paths',
    default=False,
    show_default=True,
)
def init(ctx, roles_path, force):
    """Initialise new docs/ paths."""
    ansible_readme = AnsibleReadme(roles_path, should_force=force)
    ansible_readme.init_docs()


@__main__.command(context_settings=CONTEXT_SETTINGS)
@click.argument(
    'roles-path', type=click.Path(exists=True), default=pathlib.Path('.')
)
@click.option(
    '--force/--no-force',
    help='Overwrite existing README files',
    default=False,
    show_default=True,
)
@click.option(
    '-t',
    '--template',
    help='Jinja2 template for the README file.',
    default=(
        pathlib.Path(__file__).parent.absolute() / 'templates' / 'readme.md.j2'
    ),
    type=click.Path(exists=True),
    show_default=True,
)
@click.option(
    '-n',
    '--name',
    help='Generated README file name',
    default='README.md',
    show_default=True,
)
@click.pass_context
def generate(ctx, roles_path, force, template, name):
    """Generate new README files."""
    ansible_readme = AnsibleReadme(
        roles_path,
        should_force=force,
        template=template,
        readme_name=name,
        debug=ctx.obj['debug'],
    )

    ansible_readme.generate_readmes()
