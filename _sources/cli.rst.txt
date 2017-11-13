Usage: gdal-build-debug [OPTIONS] COMMAND [ARGS]...

  A command-line utility for testing your GDAL configuration and build.

Options:
  --root TEXT  root path for relative paths
  --debug      whether to include debug logs in output
  --help       Show this message and exit.

Commands:
  cli     tests for the gdal command line interface
  config  test package inclusion in the output of gdal/configure     [options]
          --cache-file


Usage: gdal-build-debug config [OPTIONS]

  Tests the the output of gdal/configure for inclusion/exclusion of
  dependencies, and supports custom regex-based testing

  EXAMPLES:

    # The command must have a reference to the output of gdal/configure:
    # any of

    test-gdal-build --root="path/to/gdal/directory" config [...]
    PATH_TO_GDAL_CONFIG_LOG="..." test-gdal-build config [...]
    test-gdal-build test --path-to-config-log="..." [...]

    # search the configure output for included/excluded packages

    test-gdal-build --with foo --with bar --without baz

    # or

    TEST_GDAL_CONFIGURED_WITH="foo bar"
    TEST_GDAL_CONFIGURED_WITHOUT="baz"
    test-gdal-build config

    # use custom regex to search the configuration log
    # (ironically not gdal/config.log)

    # run case-insensitive tests on lines including the search prefix
    test-gdal-build config --search postgis:::(yes)|(no)|(internal)
    test-gdal-build config --search postgis:::(?P<fail>no)|(?P<success>yes)
    # or test every line
    test-gdal-build config --search "postgis\.\.\.\s(yes)|(no)|(internal)"

Options:
  --path-to-config-log PATH  a relative or absolute path to the logged output
                             of gdal/configure
  --with <package...>        Searches the output of gdal/configure to ensure
                             packages are      present.
  --without <package...>     Searches the output of gdal/configure to ensure
                             packages are absent
  --search <regex...>        case-insensitive python regex searches of the
                             form:
                               "match_line:::(success)|(failure)|(pass)"
                             match_line: a name that if matched will run the
                             test
                             
                             ::: an optional separator to treat 1 as a
                             --with option
                             
                             success The match group that
                             indicates the test succeeded (     optionally
                             named with success)
                             
                             failure: The match group
                             that indicates the test failes (     optionally
                             named fail or failure)
                             
                             pass: the match group
                             that indicates the test was not passing but
                             not fatal (optionally named pass)
                             
                             Gotchas: must
                             be quoted. Success overrides failure overrides
                             pass; named     groups override group order.
  --help                     Show this message and exit.


Usage: gdal-build-debug cli [OPTIONS]

  Tests the inclusion/exclusion of formats from the gdal command-line
  interface and installed version of gdal.

  EXAMPLES:

    # test the inclusion / exclusion of multiple gdal & ogr formats

    test-gdal-build cli --with spatialite --with pdf
    test-gdal-build cli --without geojson --without georss

    # For large or iterative tests, store the in/exclusions in environment
    # variables

    TEST_GDAL_CLI_EXCLUDES="geojson georss"
    TEST_GDAL_CLI_INCLUDES="spatialite pdf"
    test-gdal-build cli

Options:
  --with <format...>     checks a format is not present in gdal or ogr
  --without <format...>  checks a format is not present in gdal or ogr
  --version-is TEXT      Tests whether the cli version is correct via regex
  --help                 Show this message and exit.
