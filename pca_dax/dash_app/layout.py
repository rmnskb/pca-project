from dash import dcc, html
from pca_dax import data_handler as dh
import plotly.express as px

colors = {
    'background': '#111111'
    , 'text': '#7FDBFF'
}


def get_layout():
    tickers = dh.DataHandler().get_tickers()

    layout = html.Div(id='main', children=[
        html.H1(
            id='header'
            , children='Dashboard'
            , style={
                'textAlign': 'center'
                # , 'color': colors['text']
            }
        )

        , dcc.Checklist(
            id='toggle-rangeslider'
            , options=[{'label': 'Include Rangeslider'
                        , 'value': 'slider'}]
            , value=['slider']
        )

        , dcc.Dropdown(
            id='symbol-dropdown'
            , options=[{'label': k, 'value': k} for k in list(tickers)]
            # , value='SAP.DE'
            # , multi=True
        )

        , dcc.Graph(
            id='stocks-linechart'
        )
    ])

    return layout
