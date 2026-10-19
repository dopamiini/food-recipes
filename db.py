"""Helper functions to connect to database and execute queries."""
import sqlite3
from flask import g


def get_connection():
    """Create and configure connection to SQLite database."""
    con = sqlite3.connect("database.db", timeout=10)
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = sqlite3.Row
    return con


def execute(sql, params=()):
    """Executes database statement and commits changes."""
    con = get_connection()

    try:
        result = con.execute(sql, params)
        insert_id = result.lastrowid
        con.commit()
        g.last_insert_id = insert_id
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()


def last_insert_id():
    """Returns id of last inserted database row."""
    return g.last_insert_id


def query(sql, params=()):
    """Execute database query and return matching rows."""
    con = get_connection()

    try:
        result = con.execute(sql, params).fetchall()
        return result
    finally:
        con.close()
