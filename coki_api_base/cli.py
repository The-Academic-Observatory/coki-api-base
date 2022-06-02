import importlib
import os
import pathlib
import shutil
import stat
import subprocess
import tempfile

import click
import requests

from coki_api_base.openapi_renderer import OpenApiRenderer


@click.group()
def cli():
    """The COKI API base command line tool.

    COMMAND: the commands to run include:\n
      - generate-openapi-spec: generate an OpenAPI specification for a COKI API.
      - run-openapi-generator: run the openapi-generator-cli tool to create the API client for a COKI API.\n
    """
    pass


@cli.command()
@click.argument("template-file", type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.argument("output-file", type=click.Path(exists=False, file_okay=True, dir_okay=False))
@click.option("--usage-type", type=click.Choice(["cloud_endpoints", "backend", "openapi_generator"]), required=True)
def generate_openapi_spec(template_file, output_file, usage_type):
    """Generate an OpenAPI specification for a COKI API.\n

    TEMPLATE_FILE: the type of config file to generate.
    OUTPUT_FILE: the type of config file to generate.
    """

    # Render file
    renderer = OpenApiRenderer(template_file, usage_type=usage_type)
    render = renderer.render()

    # Save file
    with open(output_file, mode="w") as f:
        f.write(render)


@cli.command()
@click.argument("template-file", type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.argument("api-package-dir", type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.argument("api-docs-dir", type=click.Path(exists=True, file_okay=False, dir_okay=True))
def run_openapi_generator(template_file, api_package_dir, api_docs_dir):
    api_package_name = os.path.basename(api_package_dir)
    installation_dir = os.path.join(str(pathlib.Path.home()), "bin", "openapitools")

    # Install openapi-generator-cli if not installed yet
    if not openapi_generator_exists(installation_dir):
        install_openapi_generator(installation_dir)

    with tempfile.TemporaryDirectory() as tmp:
        # Generate OpenAPI specification
        openapi_path = os.path.join(tmp, "openapi.yaml")
        openapi_specification = OpenApiRenderer(template_file, usage_type="openapi_generator").render()
        with open(openapi_path, mode="w") as f:
            f.write(openapi_specification)

        # Move openapi config file to doc directory for REST API specification
        shutil.copyfile(openapi_path, os.path.join(api_docs_dir, "openapi.yaml"))

        # Generate OpenAPI Python client
        call_openapi_generator(installation_dir, tmp, openapi_path, api_package_name)

        # Massage files into correct directory
        move_client_files(tmp, api_package_dir, api_docs_dir, api_package_name)


def move_client_files(tmp_dir, api_dir, docs_dir, package_name):
    """

    :param tmp_dir:
    :param api_dir:
    :param docs_dir:
    :param package_name:
    :return:
    """
    source_dir = os.path.join(tmp_dir, "output", package_name)

    # Copy read the docs files
    source_readme_file = os.path.join(source_dir, "client_README.md")
    dest_readme_file = os.path.join(docs_dir, "api_client.md")
    shutil.copyfile(source_readme_file, dest_readme_file)

    source_docs_dir = os.path.join(source_dir, "client", "docs")
    shutil.copytree(source_docs_dir, docs_dir, dirs_exist_ok=True)

    # Remove moved docs dir and empty models + apis directories
    shutil.rmtree(os.path.join(source_dir, "client", "docs"))
    shutil.rmtree(os.path.join(source_dir, "client", "apis"))
    shutil.rmtree(os.path.join(source_dir, "client", "models"))

    # Copy remaining client files
    source_client_dir = os.path.join(source_dir, "client")
    dest_client_dir = os.path.join(api_dir, "client")
    shutil.copytree(source_client_dir, dest_client_dir, dirs_exist_ok=True)


def call_openapi_generator(installation_dir, tmp_dir, openapi_path, package_name):
    """

    :param installation_dir:
    :param tmp_dir:
    :param openapi_path:
    :param package_name:
    :return:
    """
    openapi_generator_dir = module_file_path("coki_api_base.openapi_generator")
    templates_dir = os.path.join(openapi_generator_dir, "templates")
    config_path = os.path.join(openapi_generator_dir, "api-config.yaml")

    output_dir = os.path.join(tmp_dir, "output")
    os.makedirs(output_dir)
    # TODO update template with specific README install package info
    proc = subprocess.Popen(
        [
            "./openapi-generator-cli",
            "generate",
            "-i",
            openapi_path,
            "-g",
            "python",
            "-c",
            config_path,
            "-t",
            templates_dir,
            f"--additional-properties=packageName={package_name}.client",
            "-o",
            output_dir,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=installation_dir,
    )
    output, error = proc.communicate()
    print(output.decode("UTF-8"))


def install_openapi_generator(installation_dir):
    """

    :param installation_dir:
    :return:
    """
    print("Installing openapi-generator-cli")
    os.makedirs(installation_dir, exist_ok=True)
    openapi_generator_path = os.path.join(installation_dir, "openapi-generator-cli")

    # Download file
    response = requests.get(
        "https://raw.githubusercontent.com/OpenAPITools/openapi-generator/master/bin/utils/openapi-generator-cli.sh"
    )
    with open(openapi_generator_path, "wb") as f:
        f.write(response.content)

    # Make executable
    st = os.stat(openapi_generator_path)
    os.chmod(openapi_generator_path, st.st_mode | stat.S_IEXEC)

    # Install
    if openapi_generator_exists(installation_dir):
        print("Successfully installed openapi-generator-cli")
    else:
        print("Error installing openapi-generator-cli")


def openapi_generator_exists(installation_dir: str, version: str = "5.3.0") -> bool:
    """

    :param installation_dir:
    :param version:
    :return:
    """
    env = os.environ.copy()
    env["PATH"] += ":~/bin/openapitools/"
    env["OPENAPI_GENERATOR_VERSION"] = version
    try:
        proc = subprocess.Popen(
            ["./openapi-generator-cli", "version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=installation_dir,
            env=env,
        )
        output, error = proc.communicate()
        if output:
            return True
    except FileNotFoundError:
        return False
    return False


def module_file_path(module_path: str, nav_back_steps: int = -1) -> str:
    """Get the file path of a module, given the Python import path to the module.

    :param module_path: the Python import path to the module, e.g. observatory.platform.dags
    :param nav_back_steps: the number of steps on the path to step back.
    :return: the file path to the module.
    """

    module = importlib.import_module(module_path)
    file_path = pathlib.Path(module.__file__).resolve()
    return os.path.normpath(str(pathlib.Path(*file_path.parts[:nav_back_steps]).resolve()))


if __name__ == "__main__":
    cli()
