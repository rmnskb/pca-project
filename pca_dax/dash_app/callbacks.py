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
        wide_format=False
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
            title=f'Candlestick chart of {selected_stock}'
            , yaxis_title='Price'
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

        fig.update_layout(
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

        return fig

    @dashapp.callback(
        Output('mean-vol-scatterplot', 'figure')
        , Input('daily-monthly-type', 'value')
        # , Input('date-picker-range', 'start_date')
        # , Input('date-picker-range', 'end_date')
    )
    def update_scatter_graph(daily_value):
        daily_mask = (daily_value == 'Daily')
        mean_var = data_instance.create_mean_var_df(daily_freq=daily_mask)

        fig = px.scatter(
            x=mean_var['vol']
            , y=mean_var['mean']
            , color=mean_var['sector']
            , hover_name=mean_var['symbol']
        )

        fig.update_traces(customdata=mean_var['symbol'])
        fig.update_layout(margin={'l': 40, 'b': 40, 't': 40, 'r': 40}
                          # , yaxis_range=(0, 0.0015)
                          # , xaxis_range=(0, 0.04)
                          )

        return fig

    def create_ts(df, title):
        fig = px.line(
            df
            , x='date'
            , y='value'
        )

        # fig.update_traces(mode='lines+markers')

        fig.update_xaxes(showgrid=False)

        fig.add_annotation(x=0, y=0.85
                           , xanchor='left'
                           , yanchor='bottom'
                           , xref='paper'
                           , yref='paper'
                           , showarrow=False
                           , align='left'
                           , text=title)

        fig.update_layout(
            height=225
            , margin={'l': 20, 'b': 30, 'r': 10, 't': 10}
        )

        return fig

    @callback(
        Output('daily-ts', 'figure')
        , Input('mean-vol-scatterplot', 'hoverData')
    )
    def update_ts(hoverData):
        symbol = hoverData['points'][0]['hovertext']

        ts = (
            data[data['symbol'] == symbol]
            .reset_index()[['date', 'adj_close']]
            .rename(columns={'adj_close': 'value'})
        )

        title = symbol + f' Daily Time Series'

        return create_ts(ts, title)

    @callback(
        Output('daily-rts', 'figure')
        , Input('mean-vol-scatterplot', 'hoverData')
        , Input('daily-monthly-type', 'value')
    )
    def update_rts(hoverData, daily_value):
        symbol = hoverData['points'][0]['hovertext']
        if daily_value == 'Daily':
            rts = data_instance.create_daily_change()[symbol]
        else:  # daily_value == 'Monthly'
            rts = data_instance.create_monthly_change()[symbol]

        ts = (
            rts
            .rename('value')
            .reset_index()
        )

        title = symbol + f' {daily_value} Change Time Series'

        return create_ts(ts, title)

    # Function to test the correctness of the output
    # @callback(
    #     Output('hover', 'figure')
    #     , Input('mean-vol-scatterplot', 'hoverData')
    # )
    # def update_hoverdata(hoverData):
    #     print(hoverData)