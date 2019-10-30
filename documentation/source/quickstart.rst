**********
Quickstart
**********

To see what kind of output Ansible-Readme can generate, the quickest way to get
started is to run it against one of your roles or some popular role out in the
wild:

.. code-block:: bash

    $ git clone https://github.com/geerlingguy/ansible-role-mysql
    $ cd ansible-role-mysql
    $ ansible-readme generate --force

Then you can quickly preview that generated README with something like:

.. code-block:: bash

    $ pip install grip
    $ grip

Alternatively, see the `Github hosted version of the generated README file`_.
It is also worth to take notice of the new `generated docs/ directory`_ as well
(please note, the "examples" stanza has been manually copied over).

.. _`Github hosted version of the generated README file`: https://github.com/decentral1se/ansible-role-mysql/blob/ansible-readme-generated-readme/README.md
.. _generated docs/ directory: https://github.com/decentral1se/ansible-role-mysql/blob/ansible-readme-generated-readme/docs/main.yml

Ansible-Readme uses an internally managed `Jinja2`_ template file formatted as
a Markdown document which it populates with information that is
programmatically read from within the role directory specified by the given
``ROLES_PATH`` (defaults to ``.``). This is configurable.

The ``init`` sub-command aims to generate a new ``docs/`` path alongside the
conventional role directory structure (tasks, defaults, meta, etc.). Within the
``main.yml`` file, it pre-propulates place holders for defaults and examples
documentation. The ``generate`` sub-command does automatically run the ``init``
command for you.

.. _Jinja2: https://palletsprojects.com/p/jinja/
