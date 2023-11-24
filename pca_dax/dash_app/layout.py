from dash import dcc, html
from pca_dax import data_handler as dh
from datetime import datetime, date
import plotly.express as px

FIRST_DATE = '2010-01-01'
date_format = '%Y-%m-%d'


colors = {
    'background': '#111111'
    , 'text': '#7FDBFF'
}


def get_layout():
    data = dh.DataHandler()
    tickers = data.get_tickers()
    sectors = data.fetch_info_from_db()['sector'].unique().tolist()

    layout = html.Div(id='first-page', children=[
        html.Div(id='main', children=[
            html.H1(
                id='header'
                , children='Dashboard'
                , style={
                    'textAlign': 'center'
                    # , 'color': colors['text']
                }
            )
            , dcc.DatePickerRange(
                id='date-picker-range'
                , min_date_allowed=FIRST_DATE
                , max_date_allowed=datetime.today().strftime(date_format)
                # , initial_visible_date=date(date.today().year, 1, 1)
                , start_date=FIRST_DATE
                , end_date=datetime.today().strftime(date_format)
            )
        ])

        , html.Div(id='first_row', children=[
            html.Div(id='first-graph', children=[
                dcc.Dropdown(
                    id='symbol-dropdown'
                    , options=[{'label': k, 'value': k} for k in list(tickers)]
                    , value='SAP.DE'
                    # , multi=True
                )
                , dcc.Graph(
                    id='stocks-linechart'
                )
            ], className='six columns')

            , html.Div(id='second-graph', children=[
                dcc.Dropdown(
                    id='sectors-dropdown'
                    , options=[{'label': k, 'value': k} for k in list(sectors)]
                    , value=['Financial Services']
                    , multi=True
                )
                , dcc.Graph(
                    id='sectors-linechart'
                )
            ], className='six columns')
        ], className='row')

        # TODO: fix the scatterplot
        , html.Div(id='second-row', children=[
            html.Div(id='radio-filter', children=[
                dcc.RadioItems(
                    options=['Daily', 'Monthly']
                    , value='Daily'
                    , id='daily-monthly-type'
                    , labelStyle={'display': 'inline-block', 'marginTop': '5px'}
                )
            ], style={
                'width': '49%', 'float': 'right'
                , 'display': 'inline-block', 'padding': '10px 5px'
            })

            , html.Div([
                 dcc.Graph(
                    id='mean-vol-scatterplot'
                    , hoverData={'points': [{'customdata': 'SAP.DE'}]}
                )
            ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'})

            , html.Div([
                dcc.Graph(id='daily-ts')
                , dcc.Graph(id='daily-rts')
            ], style={'display': 'inline-block', 'width': '49%'})
        ])
    ])

    return layout
