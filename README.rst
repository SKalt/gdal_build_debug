================
gdal_build_debug
================


.. image:: https://img.shields.io/pypi/v/gdal_build_debug.svg
        :target: https://pypi.python.org/pypi/gdal_build_debug

.. image:: https://img.shields.io/travis/skalt/gdal_build_debug.svg
        :target: https://travis-ci.org/skalt/gdal_build_debug

.. image:: https://readthedocs.org/projects/gdal-build-debug/badge/?version=latest
        :target: https://gdal-build-debug.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/skalt/gdal_build_debug/shield.svg
     :target: https://pyup.io/repos/github/skalt/gdal_build_debug/
     :alt: Updates


A pytest suite to test whether gdal built with what you wanted.

USAGE
+++++

This is to be used on the command line::
  gdal_build_debug [gdal_source_directory] [flags]


* Free software: MIT license
* Documentation: https://gdal-build-debug.readthedocs.io.


Features
--------

* parse argv
* parse arg
* static log tests
* dynamic tests
* test fixtures to mock logs, dynamic logs

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
