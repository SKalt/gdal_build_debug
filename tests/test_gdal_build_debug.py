# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
#
# """Tests for `gdal_build_debug` package."""
#
# import pytest
# import time
#
# # from click.testing import CliRunner
#
# # from gdal_build_debug import gdal_build_debug
# # from gdal_build_debug import cli
#
# @pytest.fixture
# def log(log_name):
#     """
#     Returns an example log in its entirety.
#     """
#     with open('./fixtures/{}.log'.format(log_name)) as fixture_log_file:
#         fixture_log = fixture_log_file.read()
#     return fixture_log
#
#
# @pytest.fixture
# def make_log_static():
#     "Returns an example log from `make` in its entirety"
#     return log_static('make')
#
#
# @pytest.fixture
# def config_log_static():
#     "Returns an example log from `` in its entirety"
#     return log_static('setup')
#
#
# def log_async(log_name):
#     "mock up asynchronously outputting to stdout"
#     with open('./fixtures/{}.log'.format(log_name)) as fixture_log_file:
#         for line in fixture_log_file:
#             time.sleep(.01)
#             yield line
#
#
# def test_content(response):
#     """Sample pytest test function with the pytest fixture as an argument."""
#     # from bs4 import BeautifulSoup
#     # assert 'GitHub' in BeautifulSoup(response.content).title.string
#
#
# def test_command_line_interface():
#     """Test the CLI."""
#     runner = CliRunner()
#     result = runner.invoke(cli.main)
#     assert result.exit_code == 0
#     assert 'gdal_build_debug.cli.main' in result.output
#     help_result = runner.invoke(cli.main, ['--help'])
#     assert help_result.exit_code == 0
#     assert '--help  Show this message and exit.' in help_result.output
