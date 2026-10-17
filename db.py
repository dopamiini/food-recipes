import sqlite3
from flask import g


def get_connection():
    con = sqlite3.connect("database.db", timeout=10)
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = sqlite3.Row
    return con


def execute(sql, params=()):
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
    return g.last_insert_id


def query(sql, params=()):
    con = get_connection()

    try:
        result = con.execute(sql, params).fetchall()
        return result
    finally:
        con.close()
