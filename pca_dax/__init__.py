import os
from flask import Flask
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
URL_BASE = '/dash/'


# app factory
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY')
        , DATABASE=os.path.join(app.instance_path, 'pca_project.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    register_dashapps(app)

    return app


def register_dashapps(app):
    from pca_dax.dash_app import layout
    from pca_dax.dash_app import callbacks

    dashapp = Dash(
        __name__
        , server=app
        , url_base_pathname='/dash/'
        , external_stylesheets=[dbc.themes.LUX]
        # , external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css']
    )

    with app.app_context():
        dashapp.title = 'Dash App'
        dashapp.layout = layout.get_layout()
        callbacks.register_callbacks(dashapp)


