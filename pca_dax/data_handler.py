import time
import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime
from pca_dax import yfinance_info as yfi
from pca_dax import db

# TODO: append the latest data with the help of time delta

FIRST_DATE = '2010-01-01'
TICKERS = []
date_format = '%Y-%m-%d'


class DataHandler:
    def __init__(self, tickers=None, start_date=FIRST_DATE, end_date=None):
        self._tickers = tickers
        self._start_date = start_date
        self._end_date = end_date
        self._data = pd.DataFrame({})
        self._dly_chg = pd.DataFrame({})
        self._mth_chg = pd.DataFrame({})
        self._companies_info = pd.DataFrame({})
        # self._session = LimiterSession(per_second=1)

    def get_tickers(self):
        """
        Scrapes the constituents of 3 different size DAX indices, then adds country suffix
        :return: the list of all actual constituents of 3 indices
        """
        # TODO: add a possibility to choose from multiple indices
        if self._tickers is None:
            dax = pd.read_html(
                'https://en.wikipedia.org/wiki/DAX'
                , attrs={'id': 'constituents'}
            )[0]['Ticker'].to_list()

            mdax = pd.read_html(
                'https://en.wikipedia.org/wiki/MDAX'
                , attrs={'id': 'constituents'}
            )[0]['Symbol'].to_list()

            sdax = pd.read_html(
                'https://en.wikipedia.org/wiki/SDAX'
                , attrs={'id': 'constituents'}
            )[0]['Symbol'].to_list()

            # iterates through the lists of tickers, checks if they have the suffix,
            # adds if they don't, leaves only the unique tickers eventually
            self._tickers = set([x + '.DE' if '.DE' not in x else x for x in sum([dax, mdax, sdax], [])])

        return self._tickers

    def fetch_stocks_from_api(self) -> pd.DataFrame:
        """
        Fetches the data from Yahoo! Finance publicly available API for given tickers and date range
        :return: a pandas dataframe with given tickers and in long format
        """
        df = yf.download(
            tickers=self.get_tickers()
            , start=self._start_date
            , end=self._end_date
        )

        # removes the multiindex and move the symbols to a separate column
        self._data = df.stack().reset_index(names=['Date', 'Symbol'])

        return self._data

    def fetch_info_from_api(self) -> pd.DataFrame:
        """
        Fetches the info data from Yahoo! Finance publicly available API for given tickers
        :return: a pandas dataframe with given tickers' info
        """
        col_list = ['symbol', 'shortName', 'exchange', 'industry', 'sector', 'marketCap', 'bookValue', 'beta']
        results = []
        tickers = self.get_tickers()

        for i, ticker in enumerate(tickers):
            # tries if info about the company is available, pass if not
            try:
                symbol = yfi.Ticker(ticker)
                info = symbol.info

                results.append({key: info[key] if key in info else None for key in col_list})
            except:
                pass

            # TODO: handle the requests in better fashion
            time.sleep(3)

        self._companies_info = pd.DataFrame(results)

        return self._companies_info

    def fetch_stocks_from_db(self, price_type: str ='adj_close', format:str = 'wide') -> pd.DataFrame:
        # sets today's date if the end date is missing or if it is in the future
        if self._end_date is None or self._end_date.strftime(date_format) > datetime.today():
            self._end_date = datetime.today().strftime(date_format)

        # creates connection and reads stocks data with function arguments
        with db.create_connection() as conn:
            self._data = pd.read_sql(
                f"""
                    SELECT date, symbol, {price_type}
                    FROM stocks
                    WHERE date BETWEEN '{self._start_date}' AND '{self._end_date}'
                    AND symbol IN {tuple(self.get_tickers())}
                """
                , con=conn
                , parse_dates={'date': {'format': '%Y-%m-%d'}}
                , index_col='date'
            )

        if format == 'wide':
            self._data = (self._data
                          .pivot_table(index='date', values=f'{price_type}', columns='symbol')
                          .rename_axis(columns=None))

        return self._data

    def fetch_info_from_db(self) -> pd.DataFrame:
        with db.create_connection() as conn:
            self._companies_info = pd.read_sql(
                f"""
                    SELECT *
                    FROM companies
                    WHERE symbol IN {tuple(self.get_tickers())} AND sector IS NOT NULL
                """
                , con=conn
            )

        return self._companies_info

    def preprocess(self) -> pd.DataFrame:
        """
        Initialises the index as a datetime object,
        drops any stocks that have more than 1% of whole time window missing,
        forward fills the remained stocks

        :return: Returns a preprocessed pd.DataFrame object
        """
        if self._data.empty:
            self.fetch_stocks_from_db()

        self._data.index = pd.to_datetime(self._data.index)

        if isinstance(self._data, pd.DataFrame):
            self._data = self._data.dropna(
                axis=1
                , thresh=int(0.99*len(self._data))
            )
        elif isinstance(self._data, pd.Series):
            self._data = self._data.dropna()

        if self._data.isna().any().any():
            self._data = self._data.fillna(method='ffill')

        return self._data

    def create_daily_change(self) -> pd.DataFrame:
        """
        Creates return series from wide stocks data (please choose one price type)
        :return: a dataframe with returns for given price type
        """
        self.preprocess()

        self._dly_chg = self._data.pct_change(1)
        self._dly_chg = self._dly_chg.dropna()

        return self._dly_chg

    def create_monthly_change(self) -> pd.DataFrame:
        """
        Converts daily returns to monthly returns
        :return:
        """
        if self._dly_chg.empty:
            _dly_chg = self.create_daily_change()
        else:
            _dly_chg = self._dly_chg

        self._mth_chg = _dly_chg.resample('M').agg(lambda x: (x + 1).prod() - 1)

        return self._mth_chg



