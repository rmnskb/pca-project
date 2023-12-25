from dash import Input, Output, callback
from pca_dax import data_handler as dh
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from pca_dax.common_variables import FIRST_DATE, DATE_FORMAT, COLORS


def get_date_mask(data, start_date, end_date):
    if start_date is not None and end_date is not None:
        date_mask = (data.index > start_date) & (data.index < end_date)
    elif start_date is not None:
        date_mask = (data.index > start_date) & (data.index < datetime.today().strftime(DATE_FORMAT))
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
    rts = data_instance.create_daily_change()
    mrts = data_instance.create_monthly_change()

    @dashapp.callback(
        Output('stocks-linechart', 'figure')
        , Input('symbol-dropdown', 'value')
        , Input('date-picker-range', 'start_date')
        , Input('date-picker-range', 'end_date')
    )
    def update_candlestick_graph(selected_stock, start_date, end_date):
        date_mask = get_date_mask(data, start_date, end_date)

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
            title=f"{selected_stock}"
            , title_font=dict(size=18, color=COLORS['white'])
            , paper_bgcolor=COLORS['bgcolor']
            , plot_bgcolor=COLORS['bgcolor']
        )

        fig.update_xaxes(
            showline=True
            , showgrid=True
            , zeroline=True
            , title_font=dict(size=16, color=COLORS['white'])
            , tickfont=dict(size=14, color=COLORS['white'])
            , title=''
        )

        fig.update_yaxes(
            showline=True
            , showgrid=True
            , zeroline=False
            , title='Price'
            , title_font=dict(size=16, color=COLORS['white'])
            , tickfont=dict(size=14, color=COLORS['white'])
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
            , color_discrete_sequence=COLORS['palette']
        )

        fig.update_layout(
            # title='German Market Stock Prices by Sector'
            # , title_font=dict(size=18, color=COLORS['white'])
            legend_title_text='Sector'
            , legend_font=dict(size=12, color=COLORS['white'])
            , paper_bgcolor=COLORS['bgcolor']
            , plot_bgcolor=COLORS['bgcolor']
            , legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

        fig.update_xaxes(
            showline=True
            , showgrid=True
            , zeroline=True
            , title='Date'
            , title_font=dict(size=16, color=COLORS['white'])
            , tickfont=dict(size=14, color=COLORS['white'])
        )

        fig.update_yaxes(
            showline=True
            , showgrid=True
            , zeroline=False
            , title='Price'
            , title_font=dict(size=16, color=COLORS['white'])
            , tickfont=dict(size=14, color=COLORS['white'])
        )

        return fig

    @dashapp.callback(
        Output('mean-vol-scatterplot', 'figure')
        , Input('daily-monthly-type', 'value')
    )
    def update_scatter_graph(daily_value):
        daily_mask = (daily_value == 'Daily')
        mean_var = data_instance.create_mean_var_df(daily_freq=daily_mask)

        fig = px.scatter(
            x=mean_var['vol']
            , y=mean_var['mean']
            , color=mean_var['sector']
            , hover_name=mean_var['symbol']
            , color_discrete_sequence=COLORS['palette']
        )

        fig.update_traces(customdata=mean_var['symbol'])
        fig.update_layout(margin={'l': 40, 'b': 40, 't': 40, 'r': 40}
                          # , title='Mean-Variance Plot of German Stocks'
                          # , title_font=dict(size=18, color=COLORS['white'])
                          , legend_title_text='Sector'
                          , legend_font=dict(size=12, color=COLORS['white'])
                          , paper_bgcolor=COLORS['bgcolor']
                          , plot_bgcolor=COLORS['bgcolor']
                          )

        fig.update_xaxes(
            showline=True
            , showgrid=True
            , zeroline=True
            , title='Volatility'
            , title_font=dict(size=16, color=COLORS['white'])
            , tickfont=dict(size=14, color=COLORS['white'])
        )

        fig.update_yaxes(
            showline=True
            , showgrid=True
            , zeroline=False
            , title='Mean Return'
            , title_font=dict(size=16, color=COLORS['white'])
            , tickfont=dict(size=14, color=COLORS['white'])
        )

        return fig

    def create_ts(df, title):
        fig = px.line(
            df
            , x='date'
            , y='value'
            , color_discrete_sequence=[COLORS['palette'][3]]
        )

        fig.update_layout(
            height=250
            # , margin={'l': 20, 'b': 30, 'r': 10, 't': 10}
            , title=title
            , title_font=dict(size=14, color=COLORS['white'])
            , paper_bgcolor=COLORS['bgcolor']
            , plot_bgcolor=COLORS['bgcolor']
        )

        fig.update_xaxes(
            showline=True
            , showgrid=False
            , zeroline=True
            , title='Date'
            , title_font=dict(size=12, color=COLORS['white'])
            , tickfont=dict(size=10, color=COLORS['white'])
        )

        fig.update_yaxes(
            showline=True
            , showgrid=True
            , zeroline=False
            , title='Value'
            , title_font=dict(size=12, color=COLORS['white'])
            , tickfont=dict(size=10, color=COLORS['white'])
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
            df = rts[symbol]
        else:  # daily_value == 'Monthly'
            df = mrts[symbol]

        ts = (
            df
            .rename('value')
            .reset_index()
        )

        title = symbol + f' {daily_value} Change Time Series'

        return create_ts(ts, title)
