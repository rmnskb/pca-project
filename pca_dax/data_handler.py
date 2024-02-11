import time
import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime
from pca_dax import yfinance_info as yfi
from pca_dax import db
from pca_dax.common import FIRST_DATE, DATE_FORMAT


class DataHandler:
    def __init__(self, tickers=None, start_date=FIRST_DATE, end_date=None):
        # Variables initiation
        self._tickers = tickers
        self._start_date = start_date
        self._end_date = end_date
        self._data = pd.DataFrame({})
        self._dly_chg = pd.DataFrame({})
        self._mth_chg = pd.DataFrame({})
        self._companies_info = pd.DataFrame({})
        self._mean_std = pd.DataFrame({})

    def get_tickers(self) -> set[str]:
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

    def fetch_stocks_from_db(self, price_type: str = 'adj_close', wide_format: bool = True) -> pd.DataFrame:
        """
        Fetches data from database for given stocks and given timeframe
        :param price_type: price types, such as low, high, close, adj_close.
            Multiple types can be chosen in a string by separating by comma.
        :param wide_format: False if stocks should be in a column, with price types as columns.
            True if stocks should be as columns, with one price type on a given date.
        :return: 
        """
        # sets today's date if the end date is missing or if it is in the future
        if self._end_date is None or datetime.strptime(self._end_date, DATE_FORMAT) > datetime.today():
            self._end_date = datetime.today().strftime(DATE_FORMAT)

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

        if wide_format:
            self._data = (self._data
                          .pivot_table(index='date', values=f'{price_type}', columns='symbol')
                          .rename_axis(columns=None))

        return self._data

    def fetch_info_from_db(self, tickers=None) -> pd.DataFrame:
        """
        Fetches data about companies from an initialised database.
        :param tickers: List of tickers to be retrieved the information for
        :return: returns a Dataframe with the desired companies' information
        """
        if tickers is None:
            tckrs = self.get_tickers()
        else:
            tckrs = tickers

        with db.create_connection() as conn:
            self._companies_info = pd.read_sql(
                f"""
                    SELECT *
                    FROM companies
                    WHERE symbol IN {tuple(tckrs)} AND sector IS NOT NULL
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

        data = self.fetch_stocks_from_db(price_type='adj_close', wide_format=True)

        data.index = pd.to_datetime(data.index)

        if isinstance(data, pd.DataFrame):
            data = data.dropna(
                axis=1
                , thresh=int(0.9*len(data))
            )
        elif isinstance(data, pd.Series):
            data = data.dropna()

        if data.isna().any().any():
            data = data.ffill()

        return data

    def create_daily_change(self) -> pd.DataFrame:
        """
        Creates return series from wide stocks data (please choose one price type, default is adj_close)
        :return: a dataframe with returns for given price type
        """
        data = self.preprocess()
        dly_chg = data.pct_change(1)
        self._dly_chg = dly_chg.dropna()

        return self._dly_chg

    def create_monthly_change(self) -> pd.DataFrame:
        """
        Converts daily returns to monthly returns
        """
        if self._dly_chg.empty:
            _dly_chg = self.create_daily_change()
        else:
            _dly_chg = self._dly_chg

        self._mth_chg = _dly_chg.resample('M').agg(lambda x: (x + 1).prod() - 1)

        return self._mth_chg

    def create_mean_var_df(self, daily_freq: bool = True) -> pd.DataFrame:
        """
        Create a dataframe containing data about stocks' mean return and variance, and the respective sectors
        :param daily_freq: boolean, True if you want to use daily price change frequency, False if monthly
        :return: returns a df with given frequency's mean, variance and sectors
        """
        if daily_freq:
            rts = self.create_daily_change()
        else:
            rts = self.create_monthly_change()

        stds = rts.std()
        means = rts.mean()

        self._mean_std = (pd.DataFrame(
                data={'mean': means, 'vol': stds}
                , columns=['mean', 'vol']
            ).reset_index()
            .merge(
                self.fetch_info_from_db()[['symbol', 'sector']]
                , left_on='index'
                , right_on='symbol'
            )[['symbol', 'mean', 'vol', 'sector']]
        )

        return self._mean_std


class PCA:
    def __init__(self, data: pd.DataFrame = None):
        if data is None:
            self._data = DataHandler().create_daily_change()
        else:
            self._data = data

        self._tickers = data.columns
        self._components = pd.DataFrame([])
        self._eigenvalues = None
        self._explained_variance = None
        self._loadings_sectors = pd.DataFrame([])
        self._transposed_loadings = pd.DataFrame([])

    def fit(self, cov_base: bool = False, n_comp: int = 10) -> pd.DataFrame:
        """
        Fit a PCA model to the given data
        :param cov_base: use covariance matrix as an underlying base for PCA
        :param n_comp: number of components to retain after fitting
        :return: returns a Dataframe containing data about components, where the columns are the components and
            the indices are the given tickers.
        """
        df = self._data

        df_demeaned = df - df.mean(axis=0)

        if cov_base:
            mtrx = df_demeaned.cov()
        else:
            mtrx = df_demeaned.corr()

        eigvls, eigvecs = np.linalg.eigh(mtrx)

        idx = np.argsort(eigvls)[::-1]
        sorted_eigvls = eigvls[idx]
        sorted_eigvecs = eigvecs[:, idx]

        components_names = ['PC' + str(pc) for pc in range(1, n_comp + 1)]

        self._components = pd.DataFrame(
            sorted_eigvecs[:, :n_comp]
            , columns=components_names
            , index=self._tickers
        )

        self._explained_variance = eigvls[:n_comp] / eigvls.sum()
        self._eigenvalues = sorted_eigvls

        return self._components

    def combine_loadings_sectors(self, cov_base: bool = False, n_comp: int = 10) -> pd.DataFrame:
        """
        Combine components' loadings with respective tickers' sectors
        :param cov_base: use covariance matrix as an underlying base for PCA, passes it further to fit method
        :param n_comp: number of components to retain after fitting, passes it further to fit method
        :return: return a Dataframe
        """
        ldngs = self.fit(cov_base=cov_base, n_comp=n_comp)
        tickers = self._components.index.tolist()

        with db.create_connection() as conn:
            sectors = pd.read_sql(
                f"""
                    SELECT symbol, sector
                    FROM companies
                    WHERE symbol IN {tuple(tickers)}
                """
                , con=conn
            )

        self._loadings_sectors = pd.concat(
            [ldngs, sectors.set_index('symbol')]
            , axis=1
            , join='inner'
        )

        return self._loadings_sectors

    def transpose_loadings_sectors(self, cov_base: bool = False, n_comp: int = 10) -> pd.DataFrame:
        """
        Transpose the Dataframe containing the loadings and their respective sectors
        :param cov_base: use covariance matrix as an underlying base for PCA,
            passes it further to combine_loadings_sectors method
        :param n_comp: number of components to retain after fitting,
            passes it further to combine_loadings_sectors method
        :return: return a Dataframe
        """
        ldngs = self.combine_loadings_sectors(cov_base=cov_base, n_comp=n_comp).reset_index()

        self._transposed_loadings = pd.melt(
            ldngs.sort_values(by=['sector'])
            , id_vars=['index', 'sector']
            , value_vars=ldngs[ldngs.columns.difference(['index', 'sector'])].columns.tolist()
            , var_name='component'
            , value_name='loading'
            , ignore_index=False
        )

        return self._transposed_loadings
