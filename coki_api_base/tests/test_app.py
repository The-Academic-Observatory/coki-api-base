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

import connexion
from coki_api_base.app import create_app
from coki_api_base.cli import module_file_path


class TestApp(unittest.TestCase):
    def test_create_app(self):
        openapi_spec_path = os.path.join(module_file_path("coki_api_base.fixtures"), "openapi.yaml.jinja2")

        # Test creating app without custom config
        app = create_app(openapi_spec_path)
        self.assertIsInstance(app, connexion.App)
        self.assertTrue(app.app.config["JSON_SORT_KEYS"])

        # Test creating app with custom config
        app = create_app(openapi_spec_path, config={"JSON_SORT_KEYS": False})
        self.assertIsInstance(app, connexion.App)
        self.assertFalse(app.app.config["JSON_SORT_KEYS"])
