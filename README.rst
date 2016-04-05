fluentcms-forms-builder
=======================

django-forms-builder_ content plugins for django-fluent-contents_

.. image:: https://img.shields.io/pypi/v/fluentcms-forms-builder.svg
    :target: https://pypi.python.org/pypi/fluentcms-forms-builder/

.. image:: https://img.shields.io/pypi/dm/fluentcms-forms-builder.svg
    :target: https://pypi.python.org/pypi/fluentcms-forms-builder/

.. image:: https://img.shields.io/github/license/bashu/fluentcms-forms-builder.svg
    :target: https://pypi.python.org/pypi/fluentcms-forms-builder/

.. image:: https://landscape.io/github/bashu/fluentcms-forms-builder/develop/landscape.svg?style=flat
    :target: https://landscape.io/github/bashu/fluentcms-forms-builder/develop

Installation
============

First install the module, preferably in a virtual environment. It can be installed from PyPI:

.. code-block:: shell

    pip install fluentcms-forms-builder

Backend Configuration
---------------------

First make sure the project is configured for both django-fluent-contents_ and django-forms-builder_.

Then add the following settings:

.. code-block:: python

    INSTALLED_APPS += (
        'fluentcms_forms_builder',
    )

The database tables can be created afterwards:

.. code-block:: shell

    python ./manage.py migrate

Now, the ``FormPlugin`` can be added to your ``PlaceholderField`` and
``PlaceholderEditorAdmin`` admin screens.

Frontend Configuration
----------------------

If needed, the HTML code can be overwritten by redefining ``fluentcms_forms_builder/form.html``.

Contributing
------------

If you like this module, forked it, or would like to improve it, please let us know!
Pull requests are welcome too. :-)

.. _django-fluent-contents: https://github.com/edoburu/django-fluent-contents
.. _django-forms-builder_: https://github.com/stephenmcd/django-forms-builder
