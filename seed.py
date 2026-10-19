"""This module resets the database."""
import os
import sqlite3

DATABASE = "database.db"

if os.path.exists(DATABASE):
    os.remove(DATABASE)

connection = sqlite3.connect(DATABASE)

with open("schema.sql", "r", encoding="utf-8") as file:
    connection.executescript(file.read())

with open("init.sql", "r", encoding="utf-8") as file:
    connection.executescript(file.read())

connection.close()

print("Database reset and initialized successfully.")
