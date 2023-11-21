from dash import Input, Output, callback
from pca_dax import data_handler as dh
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

FIRST_DATE = '2010-01-01'
date_format = '%Y-%m-%d'


def get_date_mask(data, start_date, end_date):
    if start_date is not None and end_date is not None:
        date_mask = (data.index > start_date) & (data.index < end_date)
    elif start_date is not None:
        date_mask = (data.index > start_date) & (data.index < datetime.today().strftime(date_format))
    elif end_date is not None:
        date_mask = (data.index > FIRST_DATE) & (data.index < end_date)
    else:
        date_mask = True

    return date_mask


def register_callbacks(dashapp):
    data_instance = dh.DataHandler(
        start_date=FIRST_DATE
    )
    data = data_instance.fetch_stocks_from_db(
        format='long'
        , price_type='open, high, low, close, adj_close'
    )
    info_data = data_instance.fetch_info_from_db()[['symbol', 'sector']]

    @dashapp.callback(
        Output('stocks-linechart', 'figure')
        , Input('symbol-dropdown', 'value')
        # , Input('toggle-rangeslider', 'value')
        , Input('date-picker-range', 'start_date')
        , Input('date-picker-range', 'end_date')
    )
    def update_candlestick_graph(selected_stock, start_date, end_date):
        date_mask = get_date_mask(data, start_date, end_date)

        # filtered_data = data[data.symbol.isin(selected_stock)]
        filtered_data = data[
                (data.symbol == selected_stock)
                & date_mask
            ]

        fig = go.Figure(go.Candlestick(
            x=filtered_data.index
            , open=filtered_data.open
            , high=filtered_data.high
            , low=filtered_data.low
            , close=filtered_data.close
        ))

        fig.update_layout(
            # xaxis_rangeslider_visible='slider' in slider_value
        )

        return fig

    @dashapp.callback(
        Output('sectors-linechart', 'figure')
        , Input('sectors-dropdown', 'value')
        , Input('date-picker-range', 'start_date')
        , Input('date-picker-range', 'end_date')
    )
    def update_sectors_graph(selected_sector, start_date, end_date):
        mean_by_sector = (
            data
            .reset_index()[['date', 'symbol', 'adj_close']]
            .merge(
                info_data
                , left_on='symbol'
                , right_on='symbol'
            )[['date', 'adj_close', 'sector']]
            .groupby(by=['date', 'sector'])
            .mean()
            .reset_index('sector')
        )

        date_mask = get_date_mask(mean_by_sector, start_date, end_date)

        filtered_data = mean_by_sector[
            mean_by_sector['sector'].isin(selected_sector)
            & date_mask
        ]

        fig = px.line(
            filtered_data
            , x=filtered_data.index
            , y='adj_close'
            , color='sector'
            , title='German Market Stock Prices by Sector'
        )

        return fig
