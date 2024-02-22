from dash import dcc, html
import dash_bootstrap_components as dbc
from pca_dax import data_handler as dh
from datetime import datetime
from pca_dax.common import (
    FIRST_DATE
    , DATE_FORMAT
    , COLORS
    , HOME_URL_BASE
    , PCA_URL_BASE
    , get_info_button
    , get_header
    , get_footer
)


def get_layout():
    data = dh.DataHandler()
    tickers = data.get_tickers()
    sectors = data.fetch_info_from_db()['sector'].unique().tolist()

    layout = dbc.Container([
        get_header(pca_active=False)

        , dbc.Row([
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
                , dcc.DatePickerRange(
                    id='date-picker-range'
                    , min_date_allowed=FIRST_DATE
                    , max_date_allowed=datetime.today().strftime(DATE_FORMAT)
                    , start_date=FIRST_DATE
                    , end_date=datetime.today().strftime(DATE_FORMAT)
                )
            ])
        ]
            , style={'width': '20rem'}
            , className='m-2'
        )


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

                            , get_info_button(
                                button_id='candles-tooltip'
                                , title='This graph shows candlestick chart of daily returns of a selected stock '
                                        'over the chosen time period. The range below can be used to zoom into '
                                        'particular time frame.'
                            )

                            , dcc.Dropdown(
                                id='symbol-dropdown'
                                , options=[{'label': k, 'value': k} for k in list(tickers)]
                                , value='SAP.DE'
                                , placeholder='Select a symbol'
                                # , style={'width': '85%'}
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

                            , get_info_button(
                                button_id='sectors-tooltip'
                                , title='This chart shows and compares mean daily returns of selected sectors '
                                        'over the chosen time period'
                            )

                            , dcc.Dropdown(
                                id='sectors-dropdown'
                                , options=[{'label': k, 'value': k} for k in list(sectors)]
                                , value=['Financial Services']
                                # , style={'width': '85%'}
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

                            , get_info_button(
                                button_id='mean-var-tooltip'
                                , title='These charts show the mean - variance distribution of selected stocks '
                                        'over all time period. You can choose either daily or monthly returns '
                                        'as a basis for the graph. When you hover over one of the stocks, '
                                        'the graphs on the right will be updated accordingly. '
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
                                , hoverData={'points': [{'hovertext': 'SAP.DE', 'curveNumber': 3}]}
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

        , get_footer()
    ], fluid=True, className='graph-container')

    return layout
