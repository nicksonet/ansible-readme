.. _header:

.. image:: http://unmaintained.tech/badge.svg
  :target: http://unmaintained.tech
  :alt: No Maintenance Intended

**************
ansible-readme
**************

.. image:: https://img.shields.io/badge/license-GPL-brightgreen.svg
   :target: LICENSE
   :alt: Repository license

.. image:: https://badge.fury.io/py/ansible-readme.svg
   :target: https://badge.fury.io/py/ansible-readme
   :alt: PyPI package

.. image:: https://travis-ci.com/pycontribs/ansible-readme.svg?branch=master
   :target: https://travis-ci.com/pycontribs/ansible-readme
   :alt: Travis CI result

.. image:: https://readthedocs.org/projects/ansible-readme/badge/?version=latest
   :target: https://ansible-readme.readthedocs.io/en/latest/
   :alt: Documentation status

.. image:: http://img.shields.io/liberapay/patrons/decentral1se.svg?logo=liberapay
   :target: https://liberapay.com/decentral1se
   :alt: Support badge

.. _introduction:

Generate documenting README files for Ansible roles
---------------------------------------------------

`The time is still ripe`_ (`tonk`_, June 2016 (!)) for standardised role
documentation but in the absence of this the Ansible community must step up and
try to formalise what is already being done and what should be done to document
roles.

Ansible-Readme is a tool which aims to enable the Ansible community to try and
come to a consensus on how we would like the standardisation of role
documentation to look like and what tools we need to do that. It does not
intend to be the last word but instead proposes an approach based on the needs
of the author. New approaches are welcome (let us implement them or at least
document them). In short, this is an experiment and your participation is
required.

The core principle is this: we need to generate the documentation based on the
role directory structure. This arises out of applying the `"Do One Thing and Do
It Well"`_ philosophy to developing roles. And as we have seen in practice, the
maintenance burden increases dramatically with this approach as the number of
roles increases. Whatever hand written documentation there is can quickly get
out of sync or sometimes be abandoned altogether.

Please join the discussion on `the issue tracker`_ or on IRC at ``#ansible-readme`` on Freenode.

.. _Ansible Molecule: https://molecule.readthedocs.io/en/stable/
.. _"Do One Thing and Do It Well": https://en.wikipedia.org/wiki/Unix_philosophy#Do_One_Thing_and_Do_It_Well
.. _The time is still ripe: https://github.com/ansible/proposals/issues/19
.. _tonk: https://github.com/tonk
.. _the issue tracker: https://github.com/pycontribs/ansible-readme/issues

.. _documentation:

Documentation
*************

* https://ansible-readme.readthedocs.io/
