from dash import dcc, html
import dash_bootstrap_components as dbc
from pca_dax.common import COLORS, HOME_URL_BASE, DASH_URL_BASE, PCA_URL_BASE, get_info_button


def get_layout():
    # nav = dbc.Nav([
    #     # dbc.NavbarBrand('Risk Sources with PCA |')
    #     html.Span('Risk Sources with PCA', style={'color': COLORS['white'], 'font-size': '175%'}, className='m-1')
    #     # , dbc.NavItem(
    #     , html.A('Home'
    #        , href=HOME_URL_BASE
    #        , style={'color': COLORS['white']}, className='m-1 nav-link'
    #     )
    #     # )
    #     , dbc.NavItem(
    #         html.A('Data'
    #                , href=DASH_URL_BASE
    #                , style={'color': COLORS['white']}, className='m-1 nav-link'
    #                )
    #     )
    #     , dbc.NavItem(
    #         html.A('PCA'
    #                , href=PCA_URL_BASE
    #                , style={'color': COLORS['hcolor']}
    #                , className='m-1 nav-link')
    #     )
    # ])

    layout = dbc.Container([
        # nav
        html.H1([
            html.Span('Risk Sources with PCA', style={'color': COLORS['white']})
            , html.Span(' | ', style={'color': COLORS['white']})
            , html.A(
                'Home'
                , href=HOME_URL_BASE
                , style={'color': COLORS['white'], 'display': 'inline'}, className='m-1 nav-link'
            )
            , html.A('Data', href=DASH_URL_BASE, style={
                'color': COLORS['white'], 'display': 'inline'
            }, className='m-1 nav-link active')
            , html.A(
                'PCA'
                , style={'color': COLORS['hcolor'], 'display': 'inline'}, className='m-1 nav-link'
            )
        ]
            , style={
                'font-size': '280%'
            }
        )
        , html.Hr(style={'color': COLORS['white']})

        , dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.Div([
                            html.Label(
                                'Choose an underlying base for PCA:'
                                , style={
                                    'color': COLORS['hcolor']
                                    , 'font-size': COLORS['font-size']
                                }
                            )
                            , dbc.RadioItems(
                                options=['Correlation', 'Covariance']
                                , id='corr-cov-type'
                                , inline=True
                                , labelClassName='btn btn-outline-primary'
                                , labelCheckedClassName='btn-primary'
                                , value='Correlation'
                            )
                        ])
                    ])
                    , className='m-2'
                    , style={'width': '28rem'})
            ])
        ])

        , dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.Div([
                            html.Label(
                                'First 5 components interactions visualised'
                                , style={
                                    'color': COLORS['hcolor']
                                    , 'font-size': COLORS['font-size']
                                }
                            )

                            , get_info_button(
                                button_id='first-five-tooltip'
                                , title='This graph visualises the interactions between'
                                        ' first five Principal Components. You can note how certain components'
                                        ' favour one sectors above others based on colour codes. You can choose either'
                                        ' correlation or covariance matrix as an underlying basis for the PCA.'
                            )

                            , dcc.Graph(
                                id='first-five'
                            )
                        ])
                    ])
                , className='m-2')
            ], width={'size': 6})

            , dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.Div([
                            html.Label(
                                'First 3 Components Visualisation'
                                , style={
                                    'color': COLORS['hcolor']
                                    , 'font-size': COLORS['font-size']
                                }
                            )

                            , get_info_button(
                                button_id='first-three-tooltip'
                                , title='This graph visualises the interactions between'
                                        ' first three Principal Components by plotting them on the same chart.'
                                        ' The dots are colour coded based on their sector. You can choose either'
                                        ' correlation or covariance matrix as an underlying basis for the PCA.'
                            )

                            , dcc.Graph(
                                id='first-three'
                            )
                        ])
                    ])
                , className='m-2')
            ], width={'size': 6})
        ])

        , dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.Div([
                            html.Label(
                                "Components' loadings visualised by sector"
                                , style={
                                    'color': COLORS['hcolor']
                                    , 'font-size': COLORS['font-size']
                                }
                            )

                            , get_info_button(
                                button_id='comp-ldngs-tooltip'
                                , title="This graph visualises the components' loadings."
                                        ' You can choose particular component in the dropdown. '
                            )

                            , dcc.Dropdown(
                                id='comp-dropdown'
                                , options=[{'label': k, 'value': k} for k in ['PC' + str(pc) for pc in range(1, 11)]]
                                , value='PC1'
                                , style={'width': '85%'}
                                , multi=False
                                # , className='nav-item dropdown'
                            )

                            , dcc.Graph(
                                id='comp-ldngs'
                            )
                        ])
                    ])
                    , className='m-2')
            ], width={'size': 6})

            , dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.Label(
                                "Commentary"
                                , style={
                                    'color': COLORS['hcolor']
                                    , 'font-size': COLORS['font-size']
                                }
                            )

                            , html.P(
                                "In the very first graph you can see..."
                            )
                        ])
                    ])
                ], className='m-2')
            ], width={'size': 6})
        ])
    ], fluid=True)

    return layout
