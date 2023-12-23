from dash import dcc, html
import dash_bootstrap_components as dbc
from pca_dax import data_handler as dh
from datetime import datetime
from pca_dax.dash_app.common_variables import FIRST_DATE, DATE_FORMAT, COLORS


def get_layout():
    layout = dbc.Container([
        html.H1([
            html.Span('Dashboard', style={'color': COLORS['white']})
            , html.Span(' | ', style={'color': COLORS['white']})
            , html.Span('PCA', style={'color': COLORS['hcolor']})
        ]
            , style={
                'font-size': '280%'
            }
        )
        , html.Hr(style={'color': COLORS['white']})

        # , html.Div(id='hidden-div', style={'display': 'none'})

        , html.Div([
            html.Label(
                'Choose an underlying base for PCA:'
                , style={
                    'color': COLORS['hcolor']
                    , 'font-size': COLORS['font-size']
                }
            )
        ])

        , dbc.Row([
            dbc.Col([
                dbc.RadioItems(
                    options=['Correlation', 'Covariance']
                    , id='corr-cov-type'
                    , inline=True
                    , labelClassName='btn btn-outline-primary'
                    , labelCheckedClassName='btn-primary'
                    , value='Correlation'
                )
            ])
        ])

        , dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label(
                        'First 5 components interactions visualised'
                        , style={
                            'color': COLORS['hcolor']
                            , 'font-size': COLORS['font-size']
                        }
                    )

                    , dcc.Graph(
                        id='first-five'
                    )
                ])
            ], width={'size': 6})
        ])

        , dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label(
                        ''
                    )

                    , dcc.Graph(
                        id='first-three'
                    )
                ])
            ], width={'size': 6})
        ])
    ], fluid=True)

    return layout