from dash import dcc, html
import dash_bootstrap_components as dbc
from pca_dax import data_handler as dh
from datetime import datetime
from pca_dax.common_variables import FIRST_DATE, DATE_FORMAT, COLORS, HOME_URL_BASE, DASH_URL_BASE, PCA_URL_BASE


def get_layout():
    data = dh.DataHandler()
    tickers = data.get_tickers()
    sectors = data.fetch_info_from_db()['sector'].unique().tolist()

    # navbar = dbc.Navbar(children=[
    #     dbc.Container([
    #         dbc.Row([
    #             html.H1([
    #                 dbc.Col([
    #                     html.Span('Risk Sources with PCA', style={'color': COLORS['white']})
    #                 ], width={'size': 3})
    #                 , dbc.Col([
    #                     html.A('Home', href='/', style={'color': COLORS['white']})
    #                 ], width={'size': 3})
    #                 , dbc.Col([
    #                     html.Span('EDA', style={'color': COLORS['hcolor']}, className='nav-link active')
    #                 ], width={'size': 3})
    #                 , dbc.Col([
    #                     html.A('PCA', href='/pca_app/', style={'color': COLORS['white']}, className='nav-link')
    #                 ], width={'size': 3})
    #             ])
    #         ], style={"textDecoration": "none"})
    #     ])
    # ], color='dark', class_name='navbar navbar-expand-lg bg-primary')

    layout = dbc.Container([
        html.H1([
            html.Span('Risk Sources with PCA', style={'color': COLORS['white']})
            , html.Span(' | ', style={'color': COLORS['white']})
            , html.A(
                'Home'
                , href=HOME_URL_BASE
                , style={'color': COLORS['white'], 'display': 'inline'}, className='m-1 nav-link'
            )
            , html.A('Data', style={
                'color': COLORS['hcolor'], 'display': 'inline'
            }, className='m-1 nav-link active')
            , html.A(
                'PCA'
                , href=PCA_URL_BASE
                , style={'color': COLORS['white'], 'display': 'inline'}, className='m-1 nav-link'
            )
            ]
            , style={
                'font-size': '280%'
            }
        )
        , html.Hr(style={'color': COLORS['white']})


        , dbc.Card(
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.Label(
                                'Pick a date range'
                                , style={
                                    'color': COLORS['hcolor']
                                    , 'font-size': COLORS['font-size']
                                }
                            )
                        ])
                    ])
                ])

                , dbc.Row([
                    dbc.Col([
                        dcc.DatePickerRange(
                            id='date-picker-range'
                            , min_date_allowed=FIRST_DATE
                            , max_date_allowed=datetime.today().strftime(DATE_FORMAT)
                            , start_date=FIRST_DATE
                            , end_date=datetime.today().strftime(DATE_FORMAT)
                        )
                    ])
                ])
            ])
        , style={'width': '20rem'}
        , className='m-2')

        , dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.Div(id='first-graph', children=[
                            html.Label(
                                "Candlestick chart of a selected stock"
                                , style={
                                    'color': COLORS['hcolor']
                                    , 'font-size': COLORS['font-size']
                                }
                            )

                            , dcc.Dropdown(
                                id='symbol-dropdown'
                                , options=[{'label': k, 'value': k} for k in list(tickers)]
                                , value='SAP.DE'
                                , placeholder='Select a symbol'
                                , style={'width': '85%'}
                            )

                            , dcc.Graph(
                                id='stocks-linechart'
                                , style={'border-radius': '15px'}
                            )
                        ])
                    ])
                , className='m-2')
            ], width={'size': 6})

            , dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.Div(id='second-graph', children=[
                            html.Label(
                                'German Market Stock Prices by Sector'
                                , style={
                                    'color': COLORS['hcolor']
                                    , 'font-size': COLORS['font-size']
                                }
                            )

                            , dcc.Dropdown(
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
                    ])
                , className='m-2')
            # ], width={'size': 5, 'offset': 1})
            ], width={'size': 6})
        ])

        , dbc.Card(
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.Label(
                                'Mean-Variance Plot of German Stocks'
                                , style={
                                    'color': COLORS['hcolor']
                                    , 'font-size': COLORS['font-size']
                                }
                            )

                            , dbc.RadioItems(
                                options=['Daily', 'Monthly']
                                , id='daily-monthly-type'
                                , inline=True
                                , labelClassName='btn btn-outline-primary'
                                , labelCheckedClassName='btn-primary'
                                , value='Monthly'
                            )
                        ])
                    ])
                ])

                , dbc.Row([
                    dbc.Col([
                        html.Div(id='third-graph', children=[
                            dcc.Graph(
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
            ])
        , className='m-2')
    ], fluid=True, className='graph-container')

    return layout
