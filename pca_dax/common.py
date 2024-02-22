from dash import html


HOME_URL_BASE = '/'
DASH_URL_BASE = '/dash/'
PCA_URL_BASE = '/pca/'

FIRST_DATE = '2010-01-01'
DATE_FORMAT = '%Y-%m-%d'
COLORS = {
    'white': '#ffffff'
    , 'hcolor': '#e3e5b1'
    , 'bgcolor': '#272a2d'
    , 'bgcolor_sec': '#343a40'
    , 'font-size': 22
    , 'palette':
        ['#00429d', '#3e67ae', '#618fbf', '#85b7ce', '#b1dfdb', '#f8c663', '#f3915f', '#e15d57', '#c2294b', '#93003a']
}


def get_info_button(button_id: str, title: str = 'Tooltip'):
    return html.Button(
        'Info'
        , id=button_id
        , title=title
        , style={'margin-left': 2, 'margin-bottom': 2.5}
        , className='btn me-md-2'
        , n_clicks=0
    )


def get_header(pca_active: bool = False) -> html.Nav:
    active_style = {
        'color': COLORS['hcolor'], 'display': 'inline'
    }

    passive_style = {
        'color': COLORS['white'], 'display': 'inline'
    }

    return html.Nav([
        html.H1([
            html.Span('Risk Sources with PCA', style={'color': COLORS['white']})
            , html.Span(' | ', style={'color': COLORS['white']})
            , html.A(
                'Home'
                , href=HOME_URL_BASE
                , style={'color': COLORS['white'], 'display': 'inline'}, className='m-1 nav-link'
            )
            , html.A('EDA'
                     , href=DASH_URL_BASE
                     , style=active_style if not pca_active else passive_style
                     , className='m-1 nav-link')
            , html.A(
                'PCA'
                , href=PCA_URL_BASE
                , style=active_style if pca_active else passive_style
                , className='m-1 nav-link'
            )
            , html.A([
                    html.I(className='fa-brands fa-github me-3 fa-1x')
                ]
                , href='https://github.com/rmnskb/pca-project'
                , style={'color': COLORS['white'], 'margin-left': '3px'}
            )
        ]
            , style={
                'font-size': '200%'
                , 'text-align': 'center'
            }
        )
        , html.Hr(style={'color': COLORS['white']})
    ])


def get_footer() -> html.Div:
    return html.Div([
        html.Hr()
        , html.P(['Created with Python, Flask and Plotly by Bogdan Romenskii, 2024'])
    ], style={'text-align': 'center'}
    )
