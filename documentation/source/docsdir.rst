************************
The docs/ role directory
************************

TODO.

This is a "new" thing in that, it's wide open for ideas.

The "docs/ directory way" could complement the "inline way".

Ansible-Readme currently expects to find the following schema:

.. code-block:: yaml

    ---

    defaults: []
    requirements: []
    examples: []

What schema would be useful here? Is it wise to duplicate the default variables
in the ``docs/main.yml`` for the purpose of documentation? If tooling can make
sure it is in sync and generated from, then perhaps it is not such a bad idea.
