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

from coki_api_base.cli import module_file_path
from coki_api_base.openapi_renderer import OpenApiRenderer
from openapi_spec_validator.exceptions import OpenAPIValidationError


class TestOpenApiRenderer(unittest.TestCase):
    def setUp(self) -> None:
        self.template_file = os.path.join(module_file_path("coki_api_base.fixtures"), "openapi.yaml.jinja2")

    def test_init(self):
        for usage_type in ["cloud_endpoints", "backend", "openapi_generator"]:
            renderer = OpenApiRenderer("template_file", usage_type)
            self.assertEqual("template_file", renderer.openapi_template_path)
            self.assertEqual(usage_type, renderer.type)

        with self.assertRaises(TypeError):
            OpenApiRenderer("template_file", "not-allowed")

    def test_render(self):
        for usage_type in ["cloud_endpoints", "backend", "openapi_generator"]:
            renderer = OpenApiRenderer(self.template_file, usage_type)
            self.assertIsInstance(renderer.render(), str)

    def test_to_dict(self):
        for usage_type in ["cloud_endpoints", "openapi_generator"]:
            renderer = OpenApiRenderer(self.template_file, usage_type)
            with self.assertRaises(AssertionError):
                renderer.to_dict()
        renderer = OpenApiRenderer(self.template_file, usage_type="backend")
        self.assertIsInstance(renderer.to_dict(), dict)

    def test_validate_spec(self):
        renderer = OpenApiRenderer(self.template_file, usage_type="backend")

        # Test valid openapi file
        renderer.validate_spec()

        # Test invalid openapi file
        with self.assertRaises(OpenAPIValidationError):
            renderer.validate_spec({"swagger": "invalid-version"})


class TestOpenApiSchema(unittest.TestCase):
    def setUp(self) -> None:
        self.template_file = os.path.join(module_file_path("coki_api_base.fixtures"), "openapi.yaml.jinja2")

    def test_validate_backend(self):
        """Test that the backend OpenAPI spec is valid"""
        renderer = OpenApiRenderer(self.template_file, usage_type="backend")
        renderer.validate_spec()

    def test_validate_cloud_endpoints(self):
        """Test that the cloud endpoints OpenAPI spec is valid"""

        renderer = OpenApiRenderer(self.template_file, usage_type="cloud_endpoints")
        renderer.validate_spec({"${host}": "api.observatory.academy", "${backend_address}": "192.168.1.1"})

    def test_validate_api_client(self):
        """Test that the API Client OpenAPI spec is valid"""

        renderer = OpenApiRenderer(self.template_file, usage_type="openapi_generator")
        renderer.validate_spec()
