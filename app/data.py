"""
fetch, clean, and commit data to db
"""

import sqlite3
from flask import current_app, g


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

def fetch_prices():
    """
    call yfinance to fetch prices
    """
    return

def clean_prices():
    """
    dedupe data, convert types (if necessary)
    """
    return

def save_prices():
    """
    commit data to DB
    """
    return

def get_prices():
    """
    read from DB
    """
    return

