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
import pathlib
import shutil
import unittest
from subprocess import PIPE
from unittest.mock import ANY, patch

from click.testing import CliRunner
from coki_api_base.cli import (
    call_openapi_generator,
    cli,
    install_openapi_generator,
    module_file_path,
    move_client_files,
    openapi_generator_exists,
)


class TestCli(unittest.TestCase):
    def test_generate_openapi_spec(self):
        """Test that the openapi spec is generated"""
        usage_types = ["cloud_endpoints", "backend", "openapi_generator"]
        fixtures_dir = module_file_path("coki_api_base.fixtures")
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

        fixtures_dir = module_file_path("coki_api_base.fixtures")
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


class TestCliFunctions(unittest.TestCase):
    def test_move_client_files(self):
        with CliRunner().isolated_filesystem() as fs:
            # Path to fixtures
            fixtures_dir = module_file_path("coki_api_base.fixtures")
            openapi_generator_output = os.path.join(fixtures_dir, "openapi_generator")

            # Create tmp dir and copy fixtures
            tmp_dir = os.path.join(fs, "tmp")
            shutil.copytree(openapi_generator_output, tmp_dir)

            # Create api dir
            api_dir = os.path.join(fs, "package")
            os.makedirs(api_dir)

            # Create docs dir
            docs_dir = os.path.join(fs, "docs")
            os.makedirs(docs_dir)

            # Move files
            move_client_files(tmp_dir, api_dir, docs_dir, package_name=os.path.basename(api_dir))

            # Check expected files in api dir
            expected_api_files = [
                "package/client/model_utils.py",
                "package/client/configuration.py",
                "package/client/rest.py",
                "package/client/__init__.py",
                "package/client/exceptions.py",
                "package/client/api_client.py",
                "package/client/test/test_observatory_api.py",
                "package/client/test/__init__.py",
                "package/client/test/test_query_response.py",
                "package/client/test/test_pit_response.py",
                "package/client/model/query_response.py",
                "package/client/model/pit_response.py",
                "package/client/model/__init__.py",
                "package/client/api/__init__.py",
                "package/client/api/observatory_api.py",
            ]
            expected_api_files = [os.path.join(fs, file) for file in expected_api_files]
            api_files = []
            for path, subdirs, files in os.walk(api_dir):
                for name in files:
                    api_files.append(os.path.join(path, name))
            expected_api_files.sort(), api_files.sort()
            self.assertListEqual(expected_api_files, api_files)

            # Check expected files in docs dir
            expected_doc_files = [
                "docs/ObservatoryApi.md",
                "docs/api_client.md",
                "docs/QueryResponse.md",
                "docs/PitResponse.md",
            ]
            expected_doc_files = [os.path.join(fs, file) for file in expected_doc_files]
            doc_files = []
            for path, subdirs, files in os.walk(docs_dir):
                for name in files:
                    doc_files.append(os.path.join(path, name))
            expected_doc_files.sort(), doc_files.sort()
            self.assertEqual(expected_doc_files, doc_files)

    @patch("subprocess.Popen")
    def test_call_openapi_generator(self, mock_subprocess):
        process_mock = unittest.mock.Mock()
        process_mock.configure_mock(**{"communicate.return_value": ("output".encode(), "error".encode())})
        mock_subprocess.return_value = process_mock

        with CliRunner().isolated_filesystem() as fs:
            # Create installation dir
            installation_dir = os.path.join(fs, "installation")
            os.makedirs(installation_dir)

            # Create tmp dir
            tmp_dir = os.path.join(fs, "tmp")
            os.makedirs(tmp_dir)

            call_openapi_generator(installation_dir, tmp_dir, "openapi_path", "package_name")

            openapi_generator_dir = module_file_path("coki_api_base.openapi_generator")
            templates_dir = os.path.join(openapi_generator_dir, "templates")
            config_path = os.path.join(openapi_generator_dir, "api-config.yaml")

            # Check that openapi generator is called with correct parameters
            mock_subprocess.assert_called_once_with(
                [
                    "./openapi-generator-cli",
                    "generate",
                    "-i",
                    "openapi_path",
                    "-g",
                    "python",
                    "-c",
                    config_path,
                    "-t",
                    templates_dir,
                    "--additional-properties=packageName=package_name.client",
                    "-o",
                    os.path.join(tmp_dir, "output"),
                ],
                stdout=PIPE,
                stderr=PIPE,
                cwd=installation_dir,
            )

    def test_install_openapi_generator(self):
        with CliRunner().isolated_filesystem() as fs:
            # Create installation dir
            installation_dir = os.path.join(fs, "installation")
            os.makedirs(installation_dir)

            # Test real installation of openapi generator tool
            success = install_openapi_generator(installation_dir)
            self.assertTrue(success)

    @patch("coki_api_base.cli.openapi_generator_exists")
    def test_mock_install_openapi_generator(self, mock_generator_exists):
        mock_generator_exists.side_effect = [True, False]
        with CliRunner().isolated_filesystem() as fs:
            # Create installation dir
            installation_dir = os.path.join(fs, "installation")
            os.makedirs(installation_dir)

            # Test mock install with success result
            success = install_openapi_generator(installation_dir)
            self.assertTrue(success)

            # Test mock install with failed result
            success = install_openapi_generator(installation_dir)
            self.assertFalse(success)

    def test_openapi_generator_exists(self):
        with CliRunner().isolated_filesystem() as fs:
            # Create installation dir
            installation_dir = os.path.join(fs, "installation")
            os.makedirs(installation_dir)

            # Test when the openapi-generator-cli shell script does not exist
            exists = openapi_generator_exists(installation_dir)
            self.assertFalse(exists)

            # Test when the openapi-generator-cli is installed
            install_openapi_generator(installation_dir)
            exists = openapi_generator_exists(installation_dir)
            self.assertTrue(exists)

            # Test with unexpected error
            with patch("subprocess.Popen") as mock_subprocess:
                process_mock = unittest.mock.Mock()
                process_mock.configure_mock(**{"communicate.return_value": ("output".encode(), "error".encode())})
                mock_subprocess.return_value = process_mock

                exists = openapi_generator_exists(installation_dir)
                self.assertFalse(exists)

    def test_module_file_path(self):
        import coki_api_base.fixtures as test_module

        # Go back one step (the default)
        expected_path = str(pathlib.Path(*pathlib.Path(test_module.__file__).resolve().parts[:-1]).resolve())
        actual_path = module_file_path("coki_api_base.fixtures", nav_back_steps=-1)
        self.assertEqual(expected_path, actual_path)

        # Go back two steps
        expected_path = str(pathlib.Path(*pathlib.Path(test_module.__file__).resolve().parts[:-2]).resolve())
        actual_path = module_file_path("coki_api_base.fixtures", nav_back_steps=-2)
        self.assertEqual(expected_path, actual_path)
