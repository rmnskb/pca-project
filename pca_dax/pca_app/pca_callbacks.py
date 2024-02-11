from dash import Input, Output
from pca_dax import data_handler as dh
import plotly.express as px
import plotly.graph_objects as go
from pca_dax.common import COLORS

theme_template = go.Layout({
    'paper_bgcolor': COLORS['bgcolor']
    , 'plot_bgcolor': COLORS['bgcolor']
    , 'scene': {
        'xaxis': {

        }
    }
})


def register_callbacks(dashapp):
    data_instance = dh.DataHandler(
        start_date='2020-01-01'
    )
    data = data_instance.create_daily_change()
    pca_instance = dh.PCA(data=data)

    @dashapp.callback(
        Output('first-five', 'figure')
        , Input('corr-cov-type', 'value')
    )
    def update_first_five_comp_graph(corr_cov):
        if corr_cov == 'Correlation':
            cov_mask = False
        else:
            cov_mask = True

        components = pca_instance.combine_loadings_sectors(cov_base=cov_mask, n_comp=10)
        # dims = components.loc[:, components.columns != 'sector'].columns.to_list()
        dims = components.loc[:, components.columns.isin(['PC' + str(pc) for pc in range(1, 6)])].columns.to_list()

        fig = px.scatter_matrix(
            components
            , dimensions=dims
            , color='sector'
            , color_discrete_sequence=COLORS['palette']
        )

        fig.update_layout(
            {'xaxis' + str(i + 1): dict(title=dict(font=dict(size=12)), color=COLORS['white']) for i in range(6)}
            , paper_bgcolor=COLORS['bgcolor']
            , plot_bgcolor=COLORS['bgcolor']
            , legend_title_text='Sector'
            , legend_font=dict(size=12, color=COLORS['white'])
        )

        fig.update_layout(
            {'yaxis' + str(i + 1): dict(title=dict(font=dict(size=12)), color=COLORS['white']) for i in range(6)}
        )

        fig.update_traces(diagonal_visible=False, showupperhalf=False)

        return fig

    @dashapp.callback(
        Output('first-three', 'figure')
        , Input('corr-cov-type', 'value')
    )
    def update_first_three_comp_graph(corr_cov):
        if corr_cov == 'Correlation':
            cov_mask = False
        else:
            cov_mask = True

        components = pca_instance.combine_loadings_sectors(cov_base=cov_mask, n_comp=10)
        dims = components.loc[:, components.columns != 'sector'].columns.to_list()

        fig = px.scatter_3d(
            components
            , x='PC1', y='PC2', z='PC3'
            , color=components['sector']
            , color_discrete_sequence=COLORS['palette']
        )

        fig.update_layout(
            paper_bgcolor=COLORS['bgcolor']
            , plot_bgcolor=COLORS['bgcolor']
            , legend_title_text='Sector'
            , legend_font=dict(size=12, color=COLORS['white'])
            , scene=dict(
                xaxis=dict(
                    title=dict(font=dict(size=12))
                    , color=COLORS['white']
                    , backgroundcolor=COLORS['bgcolor_sec']
                )
                , yaxis=dict(
                    title=dict(font=dict(size=12))
                    , color=COLORS['white']
                    , backgroundcolor=COLORS['bgcolor_sec']
                )
                , zaxis=dict(
                    title=dict(font=dict(size=12))
                    , color=COLORS['white']
                    , backgroundcolor=COLORS['bgcolor_sec']
                )
                # , bgcolor=COLORS['bgcolor_sec']
            )
        )

        return fig

    @dashapp.callback(
        Output('comp-ldngs', 'figure')
        , Input('corr-cov-type', 'value')
        , Input('comp-dropdown', 'value')
    )
    def update_components_loadings_graph(corr_cov, component):
        if corr_cov == 'Correlation':
            cov_mask = False
        else:
            cov_mask = True

        components = pca_instance.transpose_loadings_sectors(cov_base=cov_mask, n_comp=10)
        filtered_data = components[components['component'] == component]

        fig = px.bar(
            filtered_data
            , x='index'
            , y='loading'
            , color='sector'
            , color_discrete_sequence=COLORS['palette']
        )

        fig.update_layout(
            paper_bgcolor=COLORS['bgcolor']
            , plot_bgcolor=COLORS['bgcolor']
            , legend_title_text='Sector'
            , legend_font=dict(size=12, color=COLORS['white'])
        )

        fig.update_xaxes(
            title_font=dict(size=16, color=COLORS['white'])
            , tickfont=dict(size=14, color=COLORS['white'])
            , showticklabels=False
        )

        fig.update_yaxes(
            title='Loadings'
            , title_font=dict(size=16, color=COLORS['white'])
            , tickfont=dict(size=14, color=COLORS['white'])
        )

        return fig
