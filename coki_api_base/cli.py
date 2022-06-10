import os
import pathlib
import shutil
import stat
import subprocess
import tempfile

import click
import requests

from coki_api_base.openapi_renderer import OpenApiRenderer, module_file_path, render_template


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
@click.option(
    "--usage-type",
    type=click.Choice(["cloud_endpoints", "backend", "openapi_generator"]),
    required=True,
    help="What tool/service the rendered openapi specification will be used for.",
)
def generate_openapi_spec(template_file: str, output_file: str, usage_type: str):
    """Generate an OpenAPI specification for a COKI API.\n

    TEMPLATE_FILE: path to the template file for the openapi specification.
    OUTPUT_FILE: path for the rendered openapi specification file.
    """
    # Render file
    renderer = OpenApiRenderer(template_file, usage_type=usage_type)
    render = renderer.render()

    # Save file
    with open(output_file, mode="w") as f:
        f.write(render)


@cli.command()
@click.argument("output-file", type=click.Path(exists=False, file_okay=True, dir_okay=False))
@click.option(
    "--app-module-path",
    type=click.STRING,
    required=True,
    help="Python module path to the 'app' instance', e.g.: my_app_folder.server.app:app",
)
@click.option(
    "--template-file",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    default=os.path.join(module_file_path("coki_api_base.fixtures"), "Dockerfile.jinja2"),
    required=False,
    help="Path to Jinja2 template of the Dockerfile",
)
def generate_dockerfile(output_file: str, app_module_path: str, template_file: str):
    """Generate a Dockerfile for a COKI API.\n

    OUTPUT_FILE: path for the rendered Dockerfile, should be to the root of the package.
    """

    # Render file
    render = render_template(template_file, app_module_path=app_module_path)

    # Save file
    with open(output_file, mode="w") as f:
        f.write(render)


@cli.command()
@click.argument("template-file", type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.argument("api-package-dir", type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.argument("api-docs-dir", type=click.Path(exists=True, file_okay=False, dir_okay=True))
def run_openapi_generator(template_file: str, api_package_dir: str, api_docs_dir: str):
    """Generate a client library with the OpenAPI Generator for a COKI API.\n

    TEMPLATE_FILE: path to the template file for the openapi specification.
    API_PACKAGE_DIR: path to the directory of the API package.
    API_DOCS_DIR: path to the api docs directory.
    """
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


def move_client_files(tmp_dir: str, api_dir: str, docs_dir: str, package_name: str):
    """Move the generated client files to the correct directories.

    :param tmp_dir: Temporary directory with the generated client files.
    :param api_dir: Directory containing the API package.
    :param docs_dir: Directory for the docs of the API.
    :param package_name: Name of the API package.
    :return: None.
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


def call_openapi_generator(installation_dir: str, tmp_dir: str, openapi_path: str, package_name: str):
    """Call the openapi-generator-cli tool and generate the client files inside a temporary output directory.

    :param installation_dir: Directory where the openapi-generator-cli tool is installed.
    :param tmp_dir: Temporary directory used to store output
    :param openapi_path: Path to the openapi specification file
    :param package_name: Name of the API package
    :return: None.
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


def install_openapi_generator(installation_dir: str) -> bool:
    """Install the OpenAPI Generator tool

    :param installation_dir: Directory for installation
    :return: Whether the installation was successful.
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
        return True
    else:
        print("Error installing openapi-generator-cli")
        return False


def openapi_generator_exists(installation_dir: str, version: str = "5.3.0") -> bool:
    """Tries to get the version of the OpenAPI Generator tool, when it cannot find this it installs the tool if the
    openapi-generator-cli shell script is available.

    :param installation_dir: Install directory
    :param version: Version of OpenAPI Generator tool to install
    :return: Whether the OpenAPI Generator is installed
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
        # Output shows version or installation info
        if output and not error:
            return True
    # openapi-generator-cli shell script is not found & tool can not be installed
    except FileNotFoundError:
        return False
    return False


if __name__ == "__main__":
    cli()
