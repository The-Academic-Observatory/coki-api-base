# Copyright 2022 Curtin University
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Author: Aniek Roelofs

import os
import unittest
from unittest.mock import ANY, patch

from click.testing import CliRunner

from coki_api_base.cli import cli, module_file_path


class TestCli(unittest.TestCase):
    def test_generate_openapi_spec(self):
        """Test that the openapi spec is generated"""
        usage_types = ["cloud_endpoints", "backend", "openapi_generator"]
        fixtures_dir = module_file_path("tests.fixtures")
        template_file = os.path.join(fixtures_dir, "openapi.yaml.jinja2")

        runner = CliRunner()
        with runner.isolated_filesystem():
            # Test valid usage types
            for usage_type in usage_types:
                output_file = f"openapi_{usage_type}.yaml"
                result = runner.invoke(
                    cli, ["generate-openapi-spec", template_file, output_file, "--usage-type", usage_type]
                )
                self.assertEqual(os.EX_OK, result.exit_code)
                self.assertTrue(os.path.isfile(output_file))

            # Test invalid usage type
            output_file = f"openapi_invalid.yaml"
            result = runner.invoke(
                cli, ["generate-openapi-spec", template_file, output_file, "--usage-type", "invalid"]
            )
            self.assertEqual(2, result.exit_code)
            self.assertFalse(os.path.isfile(output_file))

    @patch("coki_api_base.cli.openapi_generator_exists")
    @patch("coki_api_base.cli.install_openapi_generator")
    @patch("coki_api_base.cli.call_openapi_generator")
    @patch("coki_api_base.cli.move_client_files")
    @patch("coki_api_base.cli.pathlib.Path.home")
    def test_run_openapi_generator(self, mock_home, mock_move_files, mock_call_openapi, mock_install, mock_exists):
        """Test that the right functions are called for the openapi generator"""
        mock_home.return_value = "home"
        mock_exists.side_effect = [True, False]

        fixtures_dir = module_file_path("tests.fixtures")
        template_file = os.path.join(fixtures_dir, "openapi.yaml.jinja2")

        runner = CliRunner()
        with runner.isolated_filesystem():
            os.mkdir("package_dir")
            os.mkdir("docs_dir")

            # Test when openapi generator is already installed
            result = runner.invoke(cli, ["run-openapi-generator", template_file, "package_dir", "docs_dir"])
            self.assertEqual(os.EX_OK, result.exit_code)
            mock_install.assert_not_called()
            mock_call_openapi.assert_called_once_with("home/bin/openapitools", ANY, ANY, "package_dir")
            mock_move_files.assert_called_once_with(ANY, "package_dir", "docs_dir", "package_dir")

            mock_call_openapi.reset_mock()
            mock_move_files.reset_mock()

            # Test when openapi generator is not yet installed
            result = runner.invoke(cli, ["run-openapi-generator", template_file, "package_dir", "docs_dir"])
            self.assertEqual(os.EX_OK, result.exit_code)
            mock_install.assert_called_once_with("home/bin/openapitools")
            mock_call_openapi.assert_called_once_with("home/bin/openapitools", ANY, ANY, "package_dir")
            mock_move_files.assert_called_once_with(ANY, "package_dir", "docs_dir", "package_dir")
