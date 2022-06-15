import logging

import connexion
from coki_api_base.openapi_renderer import OpenApiRenderer


def create_app(openapi_spec_path: str, config: dict = None) -> connexion.App:
    """Create a Connexion App.

    :return: the Connexion App.
    """

    logging.info("Creating app")

    # Create the application instance and update with custom config settings
    conn_app = connexion.App(__name__)
    if config:
        conn_app.app.config.update(config)

    # Add the OpenAPI specification
    builder = OpenApiRenderer(openapi_spec_path, usage_type="backend")
    specification = builder.to_dict()
    conn_app.add_api(specification)

    return conn_app
