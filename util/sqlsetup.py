# Run this file to generate the SQLite database file and tables.
# If you would like pre-fill the database with some data, you can change the value fo testdata to True.
import sqlite3
import os

# Create the SQL directory if it doesn't exist
print("Creating SQL directory...")
if not os.path.exists('sql'):
    os.makedirs('sql')


# Create the database file if it doesn't exist
con = sqlite3.connect('sql/regiment2.db')
cur = con.cursor()

# Create the tables if they don't exist
print("Creating tables...")
print("Creating users table...")
try:
    cur.execute('''CREATE TABLE users (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        username    TEXT,
        userId      INT,
        displayname TEXT,
        joined      NUMERIC
    );
    ''')
except:
    print("Users table already exists or unable to create table.")

print("Creating stockpile table...")
try:
    cur.execute('''CREATE TABLE stockpiles (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        date          NUMERIC,
        name          TEXT,
        region        TEXT,
        code          INTEGER,
        notes         TEXT,
        isPrivate     NUMERIC,
        userId        INTEGER
    );
    ''')
except:
    print("Stockpile table already exists or unable to create table.")

print("Creating active table...")
try:
    cur.execute('''CREATE TABLE active (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        username      TEXT,
        userId        INTEGER,
        wars_inactive INTEGER DEFAULT (0),
        displayname   TEXT,
        status        INTEGER,
        joined        NUMERIC
    );
    ''')
except:
    print("Active table already exists or unable to create table.")

con.commit()