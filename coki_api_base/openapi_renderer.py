# Copyright 2020 Artificial Dimensions Ltd
# Copyright 2020-2022 Curtin University
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

# Author: James Diprose, Aniek Roelofs

import importlib
import os
import pathlib
from typing import Dict

import yaml
from click.testing import CliRunner
from jinja2 import DictLoader, Environment, FileSystemLoader
from openapi_spec_validator import validate_v2_spec
from openapi_spec_validator.readers import read_from_filename


def render_template(template_path: str, child_template_path: str = None, **kwargs) -> str:
    """Render a Jinja2 template.

    :param template_path: the path to the template.
    :param child_template_path: Optional path to a child template that is included.
    :param kwargs: the keyword variables to populate the template with.
    :return: the rendered template as a string.
    """
    template_search_paths = [os.path.dirname(template_path)]
    if child_template_path:
        template_search_paths.append(os.path.dirname(child_template_path))

    # Fill template with text using common blocks
    env = Environment(loader=FileSystemLoader(template_search_paths),
                      trim_blocks=True)
    template = env.get_template(os.path.basename(template_path))

    # Render template
    rendered = template.render(**kwargs)

    return rendered


def module_file_path(module_path: str, nav_back_steps: int = -1) -> str:
    """Get the file path of a module, given the Python import path to the module.

    :param module_path: the Python import path to the module, e.g. observatory.platform.dags
    :param nav_back_steps: the number of steps on the path to step back.
    :return: the file path to the module.
    """

    module = importlib.import_module(module_path)
    file_path = pathlib.Path(module.__file__).resolve()
    return os.path.normpath(str(pathlib.Path(*file_path.parts[:nav_back_steps]).resolve()))


class OpenApiRenderer:
    def __init__(self, openapi_template_path: str, usage_type: str):
        """Construct an object that renders an OpenAPI 2 Jinja2 file.

        :param openapi_template_path: the path to the OpenAPI 2 Jinja2 template.
        :param openapi_blocks_path: the path to the template with common blocks for the OpenAPI configuration.
        :param usage_type: The usage type for which the OpenAPI file is generated, one of: cloud_endpoints, backend,
            openapi_generator
        """

        self.openapi_template_path = openapi_template_path

        allowed_types = ["cloud_endpoints", "backend", "openapi_generator"]
        if usage_type not in allowed_types:
            raise TypeError(f"Given type is not one of the allowed types: {allowed_types}")
        self.type = usage_type

    def render(self) -> str:
        """Render the OpenAPI file.

        :return: the rendered output.
        """
        # Get path to openapi blocks template
        openapi_blocks_path = os.path.join(module_file_path("coki_api_base.fixtures"), "openapi_blocks.yaml.jinja2")
        return render_template(self.openapi_template_path, openapi_blocks_path, type=self.type)

    def to_dict(self) -> Dict:
        """Render and output the OpenAPI file as a dictionary.

        :return: the dictionary.
        """

        assert self.type == "backend", "Only supported when the openapi config file is used for the backend"
        return yaml.safe_load(self.render())

    def validate_spec(self, replace_env=None):
        """Validate the rendered OpenAPI file.

        :return: None if the file is valid.
        """
        render = self.render()
        # Replace environment variables used with e.g. cloud endpoints
        if replace_env:
            for env, value in replace_env.items():
                render = render.replace(env, value)

        with CliRunner().isolated_filesystem():
            file_name = "openapi.yaml"
            with open(file_name, mode="w") as f:
                f.write(render)

            spec_dict, spec_url = read_from_filename(file_name)
        validate_v2_spec(spec_dict)
