import pandas as pd
import sqlite3
import click
from flask import current_app, g
from pca_dax import data_handler as dh
from pca_dax.common import FIRST_DATE, DATE_FORMAT
from datetime import datetime


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE']
            , detect_types=sqlite3.PARSE_DECLTYPES
        )

        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def create_connection(db='instance/pca_project.sqlite') -> sqlite3.connect:
    """
    Creates connection to sqlite database
    :param db: path to db instance
    :return: a connection to the database
    """
    conn = None

    try:
        conn = sqlite3.connect(db, detect_types=sqlite3.PARSE_DECLTYPES)
    except sqlite3.Error as e:
        print(e)

    return conn


def insert_stocks_into_db(row, conn, cursor) -> None:
    """
        Inserts stocks data into database in a given format
        :param row: row instance of pd.DataFrame
        :param conn: sqlite's connection to a database
        :param cursor: connection's cursor
        :return: void function
    """
    try:
        cursor.execute(
            """INSERT INTO stocks (date, symbol, open, high, low, close, adj_close, volume)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (row.Date.date(), row.Symbol, row.Open, row.High, row.Low, row.Close,
             row['Adj Close'], row.Volume)
        )
    except conn.IntegrityError:
        pass


def insert_info_into_db(row, conn, cursor) -> None:
    """
        Inserts info data into database in a given format
        :param row: row instance of pd.DataFrame
        :param conn: sqlite's connection to a database
        :param cursor: connection's cursor
        :return: void function
    """
    try:
        cursor.execute(
            """INSERT INTO companies 
            (symbol, name, exchange, industry, sector, market_cap, book_value, beta, stock_index)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (row.symbol, row.shortName, row.exchange, row.industry
             , row.sector, row.marketCap, row.bookValue, row.beta, row.stock_index)
        )
    except conn.IntegrityError as e:
        pass


def init_db() -> None:
    """Gets the database connection and runs an .sql database initialisation script"""
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf-8'))


def populate_stocks(index: str = 'DAX') -> None:
    """Populates the stocks table with the data from Yahoo! API"""
    with create_connection() as conn:
        c = conn.cursor()

        data = dh.DataHandler(index=index, start_date=FIRST_DATE)

        stocks_df = data.fetch_stocks_from_api()

        for i, row in stocks_df.iterrows():
            insert_stocks_into_db(row=row, conn=conn, cursor=c)

        conn.commit()


def populate_info(index: str = 'DAX') -> None:
    """Populates the info table with the data from Yahoo! API"""
    with create_connection() as conn:
        c = conn.cursor()

        data = dh.DataHandler(index=index)

        info_df = data.fetch_info_from_api()

        for i, row in info_df.iterrows():
            insert_info_into_db(row=row, conn=conn, cursor=c)
            print(f'{row.symbol} was added')

        conn.commit()


def update_stocks(index: str = 'DAX') -> None:
    """Gets the latest date from the stocks table, fills in the missing dates"""
    with create_connection() as conn:
        c = conn.cursor()

        max_date = c.execute(
            """
                SELECT MAX(date)
                FROM stocks
            """
        ).fetchone()[0]

        if datetime.strptime(max_date, DATE_FORMAT) < datetime.today():
            data = dh.DataHandler(
                index=index
                , start_date=max_date
            )

            stocks_df = data.fetch_stocks_from_api()

            for i, row in stocks_df.iterrows():
                insert_stocks_into_db(row=row, conn=conn, cursor=c)

            conn.commit()


def update_info(index: str = 'DAX') -> None:
    """Gets missing companies' data from the API and inserts it into the database"""
    tickers = dh.DataHandler(index=index).get_tickers()

    with create_connection() as conn:
        c = conn.cursor()

        c.execute(
            """
                SELECT DISTINCT symbol
                FROM companies
            """
        )

        symbols_in_db = set([row[0] for row in c.fetchall()])

        missing_vals = tickers - symbols_in_db

        if missing_vals:
            data = dh.DataHandler(tickers=missing_vals)

            info_df = data.fetch_info_from_api()

            for i, row in info_df.iterrows():
                insert_info_into_db(row=row, conn=conn, cursor=c)
                # print(f'{row.symbol} was updated successfully')

            conn.commit()


# CLI commands initiation
@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialisation complete.')


@click.command('populate-db')
@click.argument('index')
def populate_db_command(index):
    click.echo(f'Choose index {index}')
    populate_info(index=index)
    click.echo(f'Finish populating reference table for index {index}')
    populate_stocks(index=index)
    click.echo('The tables were populated successfully.')


@click.command('update-db')
@click.argument('index')
def update_db_command(index):
    click.echo(f'Choose index {index}')
    update_info(index=index)
    click.echo(f'Finish updating reference table.')
    update_stocks(index=index)
    click.echo('The database was updated successfully.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(populate_db_command)
    app.cli.add_command(update_db_command)

