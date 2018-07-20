import os

from flask import Flask
from flask_bootstrap import Bootstrap

from .views import groundtruth

# instantiate the extensions
bootstrap = Bootstrap()


def create_app():
    # instantiate the app
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='../static',
        static_url_path='/static'
    )

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions
    bootstrap.init_app(app)

    # register blueprints
    app.register_blueprint(groundtruth)

    # shell context for flask cli
    app.shell_context_processor({'app': app})

    return app
