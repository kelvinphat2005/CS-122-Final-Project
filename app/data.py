"""
fetch, clean, and commit data to db
"""

import sqlite3
from datetime import date, timedelta

import click
import pandas as pd
import yfinance as yf
from flask import current_app, g

# column order used by the prices table and by every DataFrame this module returns
PRICE_COLUMNS = ["open", "high", "low", "close", "adj_close", "volume"]

SCHEMA = """
CREATE TABLE IF NOT EXISTS prices (
    ticker    TEXT    NOT NULL,
    date      TEXT    NOT NULL,   -- ISO format YYYY-MM-DD
    open      REAL,
    high      REAL,
    low       REAL,
    close     REAL,
    adj_close REAL,
    volume    INTEGER,
    PRIMARY KEY (ticker, date)
);
"""


def get_db():
    """
    return this request's SQLite connection, opening it on first use.
    the connection is stored on g, so every function in the same request
    shares it. call this inside functions (during a request), not at import time.
    """
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
    return g.db


def close_db(exception=None):
    """
    close this request's connection, if one was opened.
    runs automatically at the end of every request (registered with
    app.teardown_appcontext in create_app).
    """
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """
    create the tables if they don't exist yet. safe to call repeatedly.
    """
    db = get_db()
    db.executescript(SCHEMA)
    db.commit()


@click.command("init-db")
def init_db_command():
    """flask init-db: create the database tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """
    hook db setup into the app: close connections after each request,
    register the init-db CLI command, and make sure the tables exist.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    with app.app_context():
        init_db()


def fetch_prices(ticker, start=None, end=None):
    """
    call yfinance to fetch daily prices for one ticker.

    start/end are 'YYYY-MM-DD' strings or date objects. start defaults to
    5 years ago, end defaults to today. end is inclusive here (yfinance's
    own end is exclusive, so we add a day).

    returns the raw yfinance DataFrame (may be empty if the ticker is invalid).
    """
    # default end date: today
    if end:
        end = pd.Timestamp(end).date()
    else:
        end = date.today()

    # default start date: 5 years before the end date
    if start:
        start = pd.Timestamp(start).date()
    else:
        start = end - timedelta(days=5 * 365)

    return yf.Ticker(ticker).history(
        start=start.isoformat(),
        end=(end + timedelta(days=1)).isoformat(),
        interval="1d",
        auto_adjust=False,  # keep both Close and Adj Close
        actions=False,      # drop Dividends / Stock Splits columns
    )


def clean_prices(df):
    """
    dedupe data, convert types (if necessary).

    takes the raw yfinance DataFrame and returns one indexed by a
    tz-naive DatetimeIndex named 'date' with columns PRICE_COLUMNS.
    """
    if df is None or df.empty:
        return pd.DataFrame(columns=PRICE_COLUMNS, index=pd.DatetimeIndex([], name="date"))

    df = df.rename(columns={
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Adj Close": "adj_close",
        "Volume": "volume",
    })
    if "adj_close" not in df.columns:
        df["adj_close"] = df["close"]
    df = df[PRICE_COLUMNS].copy()

    # normalize index to plain dates (drop timezone + time-of-day)
    idx = pd.to_datetime(df.index)
    if idx.tz is not None:
        idx = idx.tz_localize(None)
    df.index = idx.normalize()
    df.index.name = "date"

    # dedupe, sort, fill gaps, enforce types
    df = df[~df.index.duplicated(keep="last")].sort_index()
    df = df.apply(pd.to_numeric, errors="coerce").ffill()
    df = df.dropna(subset=["close"])  # leading rows with nothing to fill from
    df["volume"] = df["volume"].fillna(0).astype("int64")

    return df


def save_prices(ticker, df):
    """
    commit data to DB. existing (ticker, date) rows are overwritten,
    so re-fetching the same range never creates duplicates.

    returns the number of rows written.
    """
    if df is None or df.empty:
        return 0

    ticker = ticker.upper()
    rows = [
        (
            ticker,
            idx.strftime("%Y-%m-%d"),
            float(r.open), float(r.high), float(r.low),
            float(r.close), float(r.adj_close), int(r.volume),
        )
        for idx, r in df.iterrows()
    ]

    db = get_db()
    db.executemany(
        """
        INSERT OR REPLACE INTO prices
            (ticker, date, open, high, low, close, adj_close, volume)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        rows,
    )
    db.commit()
    return len(rows)


def get_prices(ticker, start=None, end=None):
    """
    read from DB. returns a DataFrame indexed by date (DatetimeIndex named
    'date') with columns PRICE_COLUMNS, sorted oldest -> newest.
    start/end are optional and inclusive.
    """
    query = "SELECT date, " + ", ".join(PRICE_COLUMNS) + " FROM prices WHERE ticker = ?"
    params = [ticker.upper()]
    if start:
        query += " AND date >= ?"
        params.append(pd.Timestamp(start).strftime("%Y-%m-%d"))
    if end:
        query += " AND date <= ?"
        params.append(pd.Timestamp(end).strftime("%Y-%m-%d"))
    query += " ORDER BY date"

    df = pd.read_sql_query(query, get_db(), params=params, parse_dates=["date"])
    return df.set_index("date")


def update_prices(ticker, start=None, end=None):
    """
    convenience wrapper: fetch -> clean -> save. returns rows written.
    """
    raw = fetch_prices(ticker, start, end)
    return save_prices(ticker, clean_prices(raw))
