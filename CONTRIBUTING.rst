Get started
-----------

Install `Tox`_.

.. _tox: http://tox.readthedocs.io/

Run tests
---------

.. code-block:: bash

    tox -e test

Lint source
-----------

.. code-block:: bash

    tox -e lint

Format source
-------------

.. code-block:: bash

    tox -e format

Type check source
-----------------

.. code-block:: bash

    tox -e type

Edit the documentation
----------------------

.. code-block:: bash

    tox -e docs
    tox -e docs-livereload

Release Process
---------------

Add a change entry and re-generate the changelog:

.. code-block:: bash

    $ towncrier

Make a new release tag:

.. code-block:: bash

    $ git tag x.x.x
    $ git push --tags

If you have a development install locally, you can verify:

.. code-block:: bash

    $ ansible-readme --version

Then run the release process:

.. code-block:: bash

    $ tox -e metadata-release
    $ tox -e release
