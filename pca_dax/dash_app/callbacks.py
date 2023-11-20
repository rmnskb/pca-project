from dash import Input, Output, callback
from pca_dax import data_handler as dh
import plotly.express as px
import plotly.graph_objects as go


def register_callbacks(dashapp):
    @dashapp.callback(
        Output('stocks-linechart', 'figure')
        , Input('symbol-dropdown', 'value')
        , Input('toggle-rangeslider', 'value')
    )
    def update_graph(selected_stock, slider_value):
        data = dh.DataHandler(
            start_date='2023-01-01'
        ).fetch_stocks_from_db(
            format='long'
            , price_type='open, high, low, close'
        )

        # filtered_data = data[data.symbol.isin(selected_stock)]
        filtered_data = data[data.symbol == selected_stock]

        # fig = px.line(
        #     filtered_data
        #     , x=filtered_data.index
        #     , y='adj_close'
        #     , color='symbol'
        #     , title='German Market Stock Prices in 2023'
        # )

        fig = go.Figure(go.Candlestick(
            x=filtered_data.index
            , open=filtered_data.open
            , high=filtered_data.high
            , low=filtered_data.low
            , close=filtered_data.close
        ))

        fig.update_layout(
            xaxis_rangeslider_visible='slider' in slider_value
        )

        # fig.update_xaxes(
        #     rangebreaks=[
        #         dict(bounds=['sat', 'sun'])
        #     ]
        # )

        return fig
