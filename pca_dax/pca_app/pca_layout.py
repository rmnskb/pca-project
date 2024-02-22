from dash import dcc, html
import dash_bootstrap_components as dbc
from pca_dax.common import (
    FIRST_DATE
    , DATE_FORMAT
    , COLORS
    , get_info_button
    , get_header
    , get_footer
)


def get_layout():
    layout = dbc.Container([
        get_header(pca_active=True)

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
                                "From all three graphs one can see how different are  "
                                "covariance and correlation matrices once it comes "
                                "to constructing principal components. "
                                "The covariance matrix approach clearly favours "
                                "the equities with the biggest variance, which makes sense, since "
                                "the process does not undergo the normalisation step. "
                                "The third graph shows how the first component more or less resembles "
                                "the 1/N portfolio with all the weights being almost equal. "
                                "Second component generally goes short on healthcare and technology sectors, "
                                "giving them negative loadings. Similar explanations can be found for higher order "
                                "components as well, albeit the loadings get less consistent with growing order. "
                            )
                        ])
                    ])
                ], className='m-2')
            ], width={'size': 6})
        ])

        , get_footer()
    ], fluid=True)

    return layout
