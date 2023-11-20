import pandas as pd
import sqlite3
import click
from flask import current_app, g
from pca_dax import data_handler as dh
from datetime import datetime

date_format = '%Y-%m-%d'
FIRST_DATE = '2000-01-01'


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


def create_connection(db='instance/pca_project.sqlite'):
    conn = None

    try:
        conn = sqlite3.connect(db, detect_types=sqlite3.PARSE_DECLTYPES)
    except sqlite3.Error as e:
        print(e)

    return conn


def insert_stocks_into_db(row, conn, cursor):
    try:
        cursor.execute(
            """INSERT INTO stocks (symbol, date, open, high, low, close, adj_close, volume)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (row.Symbol, row.Date.date(), row.Open, row.High, row.Low, row.Close,
             row['Adj Close'], row.Volume)
        )
    except conn.IntegrityError:
        pass


def insert_info_into_db(row, conn, cursor):
    try:
        cursor.execute(
            """INSERT INTO companies (symbol, name, exchange, industry, sector, market_cap, book_value, beta)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (row.symbol, row.shortName, row.exchange, row.industry
             , row.sector, row.marketCap, row.bookValue, row.beta)
        )
    except conn.IntegrityError as e:
        pass


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf-8'))


def populate_stocks():
    with create_connection() as conn:
        c = conn.cursor()

        data = dh.DataHandler(start_date=FIRST_DATE)

        stocks_df = data.fetch_stocks_from_api()

        for i, row in stocks_df.iterrows():
            insert_stocks_into_db(row=row, conn=conn, cursor=c)

        conn.commit()


def populate_info():
    with create_connection() as conn:
        c = conn.cursor()

        data = dh.DataHandler()

        info_df = data.fetch_info_from_api()

        for i, row in info_df.iterrows():
            insert_info_into_db(row=row, conn=conn, cursor=c)

        conn.commit()


# def populate_db():
#     with create_connection() as conn:
#         c = conn.cursor()
#
#         data = dh.DataHandler(start_date=FIRST_DATE)
#
#         stocks_df = data.fetch_stocks_from_api()
#
#         for i, row in stocks_df.iterrows():
#             try:
#                 c.execute(
#                     """INSERT INTO stocks (symbol, date, open, high, low, close, adj_close, volume)
#                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
#                     (row.Symbol, row.Date.date(), row.Open, row.High, row.Low, row.Close,
#                      row['Adj Close'], row.Volume)
#                 )
#             except conn.IntegrityError as e:
#                 continue
#
#         conn.commit()
#
#         info_df = data.fetch_info_from_api()
#
#         for i, row in info_df.iterrows():
#             try:
#                 c.execute(
#                     """INSERT INTO companies (symbol, name, exchange, industry, sector, market_cap, book_value, beta)
#                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
#                     (row.symbol, row.shortName, row.exchange, row.industry
#                      , row.sector, row.marketCap, row.bookValue, row.beta)
#                 )
#
#                 conn.commit()
#             except conn.IntegrityError as e:
#                 continue


def update_db():
    with create_connection() as conn:
        c = conn.cursor()

        max_date = c.execute(
            """
                SELECT MAX(date)
                FROM stocks
            """
        ).fetchone()[0]

        if datetime.strptime(max_date, date_format) < datetime.today():
            data = dh.DataHandler(
                start_date=max_date
            )

            stocks_df = data.fetch_stocks_from_api()

            for i, row in stocks_df.iterrows():
                insert_stocks_into_db(row=row, conn=conn, cursor=c)

            conn.commit()


@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialisation complete.')


@click.command('populate-db')
def populate_db_command():
    # populate_db()
    populate_stocks()
    populate_info()
    click.echo('The tables were populated successfully.')


@click.command('update-db')
def update_db_command():
    update_db()
    click.echo('The database was updated successfully.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(populate_db_command)
    app.cli.add_command(update_db_command)

