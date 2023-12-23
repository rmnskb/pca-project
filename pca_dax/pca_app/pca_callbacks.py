from dash import Input, Output, callback
from pca_dax import data_handler as dh
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from pca_dax.dash_app.common_variables import FIRST_DATE, DATE_FORMAT, COLORS


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

        components = pca_instance.combine_loadings_sectors(cov_base=cov_mask, n_comp=5)
        dims = components.loc[:, components.columns != 'sector'].columns.to_list()

        fig = px.scatter_matrix(
            components
            , dimensions=dims
            , color='sector'
            , color_discrete_sequence=COLORS['palette']
        )

        fig.update_layout(
            paper_bgcolor=COLORS['bgcolor']
            , plot_bgcolor=COLORS['bgcolor']
        )

        for i, label in enumerate(dims):
            fig.update_xaxes(
                tickfont=dict(size=14, color=COLORS['white'])
            )
            
            fig.update_yaxes(
                tickfont=dict(size=14, color=COLORS['white'])
            )

        # fig.update_xaxes(
        #     title_font=dict(size=16, color=COLORS['white'])
        #     , tickfont=dict(size=14, color=COLORS['white'])
        #     , title=''
        # )
        #
        # fig.update_yaxes(
        #     title_font=dict(size=16, color=COLORS['white'])
        #     , tickfont=dict(size=14, color=COLORS['white'])
        #     , title=''
        # )

        fig.update_traces(diagonal_visible=False)

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

        components = pca_instance.combine_loadings_sectors(cov_base=cov_mask, n_comp=3)
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
        )

        return fig
