import os

import flask
from flask import Flask, render_template
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from pca_dax.common import HOME_URL_BASE, DASH_URL_BASE, PCA_URL_BASE


# app factory
def create_app(test_config=None) -> flask.Flask:
    # TODO: cover the tests
    # TODO: add images to the front page and favicons
    # TODO: add descriptions to the graphs
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

    @app.route(HOME_URL_BASE)
    def hello():
        return render_template('pca_home.html')

    from . import db
    db.init_app(app)

    # TODO: Handle an empty DB case
    register_dashapps(app)

    return app


def register_dashapps(app):
    from pca_dax.dash_app import layout, callbacks
    from pca_dax.pca_app import pca_layout, pca_callbacks

    dashpage = Dash(
        __name__
        , server=app
        , url_base_pathname=DASH_URL_BASE
        , external_stylesheets=[dbc.themes.LUX, '/static/style.css']
    )

    pcapage = Dash(
        __name__
        , server=app
        , url_base_pathname=PCA_URL_BASE
        , external_stylesheets=[dbc.themes.LUX, '/static/style.css']
    )

    with app.app_context():
        dashpage.title = 'Dash App'
        dashpage.layout = layout.get_layout()
        callbacks.register_callbacks(dashpage)

        pcapage.title = 'PCA App'
        pcapage.layout = pca_layout.get_layout()
        pca_callbacks.register_callbacks(pcapage)

