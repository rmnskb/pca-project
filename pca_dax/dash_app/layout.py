from dash import dcc, html
import dash_bootstrap_components as dbc
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

    navbar = dbc.NavbarSimple(children=[
        # TODO: add navbar
    ])

    layout = dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div(id='title', children=[
                    html.H1(
                        id='header'
                        , children='Dashboard'
                        , style={
                            'textAlign': 'center'
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
            ])
        ])

        , dbc.Row([
            dbc.Col([
                html.Div(id='first-graph', children=[
                    dcc.Dropdown(
                        id='symbol-dropdown'
                        , options=[{'label': k, 'value': k} for k in list(tickers)]
                        , value='SAP.DE'
                        , style={'width': '85%'}
                    )

                    , dcc.Graph(
                        id='stocks-linechart'
                    )
                ])
            ], width={'size': 6})

            , dbc.Col([
                html.Div(id='second-graph', children=[
                    dcc.Dropdown(
                        id='sectors-dropdown'
                        , options=[{'label': k, 'value': k} for k in list(sectors)]
                        , value=['Financial Services']
                        , style={'width': '85%'}
                        , multi=True
                    )

                    , dcc.Graph(
                        id='sectors-linechart'
                    )
                ])
            ], width={'size': 5, 'offset': 1})
        ])

        , dbc.Row([
            dbc.Col([
                html.Div(id='third-graph', children=[
                    dcc.RadioItems(
                        options=['Daily', 'Monthly']
                        , value='Monthly'
                        , id='daily-monthly-type'
                        # , labelStyle={'display': 'inline-block', 'marginTop': '5px'}
                        , labelClassName='mr-2'
                    )

                    , dcc.Graph(
                        id='mean-vol-scatterplot'
                        , hoverData={'points': [{'hovertext': 'SAP.DE'}]}
                    )
                ])
            ], width={'size': 7})

            , dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(id='daily-ts')
                    ])
                ], justify='end')

                , dbc.Row([
                    dbc.Col([
                        dcc.Graph(id='daily-rts')
                    ])
                ], justify='end')
            ], width={'size': 4})
        ])
    ], fluid=True)

    # layout = dbc.Container([
    # dbc.Row([
    #     html.Div(id='first-page', children=[
    #         html.Div(id='main', children=[
    #             html.H1(
    #                 id='header'
    #                 , children='Dashboard'
    #                 , style={
    #                     'textAlign': 'center'
    #                     # , 'color': colors['text']
    #                 }
    #             )
    #             , dcc.DatePickerRange(
    #                 id='date-picker-range'
    #                 , min_date_allowed=FIRST_DATE
    #                 , max_date_allowed=datetime.today().strftime(date_format)
    #                 # , initial_visible_date=date(date.today().year, 1, 1)
    #                 , start_date=FIRST_DATE
    #                 , end_date=datetime.today().strftime(date_format)
    #             )
    #         ])
    # ])

    #         , dbc.Row([
    #             html.Div(id='first_row', children=[
    #                 dbc.Col(
    #                     html.Div(id='first-graph', children=[
    #                         dcc.Dropdown(
    #                             id='symbol-dropdown'
    #                             , options=[{'label': k, 'value': k} for k in list(tickers)]
    #                             , value='SAP.DE'
    #                             , style={'width': '85%'}
    #                             # , multi=True
    #                         )
    #                         , dcc.Graph(
    #                             id='stocks-linechart'
    #                         )
    #                     ]
    #                     )
    #                 )
    #
    #                 , dbc.Col(
    #                     html.Div(id='second-graph', children=[
    #                         dcc.Dropdown(
    #                             id='sectors-dropdown'
    #                             , options=[{'label': k, 'value': k} for k in list(sectors)]
    #                             , value=['Financial Services']
    #                             , style={'width': '85%'}
    #                             , multi=True
    #                         )
    #                         , dcc.Graph(
    #                             id='sectors-linechart'
    #                         )
    #                     ])
    #                 )
    #             ])
    #         ], align='center')
    #
    #         , html.Div(id='second-row', children=[
    #             html.Div(id='radio-filter', children=[
    #                 dcc.RadioItems(
    #                     options=['Daily', 'Monthly']
    #                     , value='Monthly'
    #                     , id='daily-monthly-type'
    #                     , labelStyle={'display': 'inline-block', 'marginTop': '5px'}
    #                 )
    #                 , dcc.Graph(
    #                     id='mean-vol-scatterplot'
    #                     , hoverData={'points': [{'hovertext': 'SAP.DE'}]}
    #                 )
    #             ], style={
    #                 'width': '60%', 'float': 'left'
    #                 , 'display': 'inline-block', 'padding': '10px 5px'
    #             })
    #
    #             # , html.Div([
    #             #
    #             # ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'})
    #
    #             , html.Div([
    #                 dcc.Graph(id='daily-ts')
    #                 , dcc.Graph(id='daily-rts')
    #             ], style={'display': 'inline-block', 'width': '35%', 'float': 'right'})
    #         ])
    #     ])
    # ], fluid=True)

    return layout
