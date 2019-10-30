Ansible_Readme 1.0.5 (2019-10-30)
=================================

Features
--------

- "Back to the top" becomes now "Back to table of contents" in the Markdown template. (#10)
- Add "Back to table of contents" to more sections for easier navigation. (#11)

Bug Fixes
---------

- Fix "#example-playbook" TOC link typo. (#9)

Improved Documentation
----------------------

- Add approaches sectiont to documentation. (#7)
- Add link to generate README file from Ansible-Readme. (#8)

Ansible_Readme 1.0.4 (2019-10-30)
=================================

Bug Fixes
---------

- Fix for overwriting docs/main.yml when ``generate --force`` is passed. (#5)


Ansible_Readme 1.0.3 (2019-10-30)
=================================

Bug Fixes
---------

- Fix Path / Str wrangling once again for Click compatibility. (#4)


Ansible_Readme 1.0.2 (2019-10-30)
=================================

Bug Fixes
---------

- Include package data (Jinja2 template) with Pypi package release. (#3)

Trivial/Internal Changes
------------------------

- Include the right classifiers and keywords for the Pypi package.


Ansible_Readme 1.0.1 (2019-10-30)
=================================

Bug Fixes
---------

- Fix ``AttributeError`` resulting from usage of pathlib.Path and the Click library. (#1)

Trivial/Internal Changes
------------------------

- Fix ``towncrier`` integration to detect the project. (#2)


Ansible_Readme 1.0.0 (2019-10-30)
=================================

Project Annoucements
--------------------

- Initial release.
