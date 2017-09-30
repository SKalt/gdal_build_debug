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


A pytest suite to test whether gdal built with the dependencies and formats you
want.

https://trac.osgeo.org/gdal/wiki/BuildingOnUnix

USAGE
+++++

This is to be used on the command line::
gdal_build_debug [OPTIONS] COMMAND [ARGS]...

Options:
--help  Show this message and exit.

Commands:
test

EXAMPLES
--------
gdal_build_debug test --formats with:postgis
gdal_build_debug test --formats without:postgis
gdal_build_debug test --formats with:postgis without:spatialite

gdal_build_debug test --dependencies with:spatialite
gdal_build_debug test --dependencies --formats with:geos with:geojson
# tests whether the configuration log includes the GEOS dependency and the command line supports the geojson format

gdal_build_debug test --version-is=2.2.*
# match the version via regex









* Free software: MIT license
* Documentation: https://gdal-build-debug.readthedocs.io.


Features
--------


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
