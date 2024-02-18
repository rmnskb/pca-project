from dash import html


HOME_URL_BASE = '/pca/home/'
DASH_URL_BASE = '/pca/dash/'
PCA_URL_BASE = '/pca/app/'

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
