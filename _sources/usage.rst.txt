=====
Usage
=====

To use gdal_build_debug's tests in a project or gdal compilation pipeline::
    from gdal_build_debug.cli_test_fns import \
    test_version_is, \ # for checking the new build version, indicating the new build is in $PATH
    main as test_cli_formats # for checking ogr and gdal format support

    from gdal_build_debug.config_test_fns import main as test_config_log
