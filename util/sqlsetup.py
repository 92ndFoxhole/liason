# Run this file to generate the SQL database and tables.
import os
import mariadb

class SQLiteConnection:
    def __init__(self, db_name):
        self.con = mariadb.connect(
            user="regimentdbuser",
            password="password",
            host="127.0.0.1",
            port=3306
        )
        
        self.cur = self.con.cursor()

    def execute(self, query, params=()):
        self.cur.execute(query, params)

    def commit(self):
        self.con.commit()

    def close(self):
        self.con.close()

db = SQLiteConnection("sql/regiment2")

db.cur.execute("CREATE DATABASE IF NOT EXISTS `regiment2` /*!40100 COLLATE 'utf8mb4_general_ci' */")
db.cur.execute("USE `regiment2`")

# Create the tables
print("Creating tables...")
print("Creating users table...")
try:
    db.cur.execute('''CREATE TABLE users (
        id          VARCHAR(36) PRIMARY KEY,
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
    db.cur.execute('''CREATE TABLE stockpiles (
        id             VARCHAR(36) PRIMARY KEY,
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
    db.cur.execute('''CREATE TABLE active (
        id            VARCHAR(36) PRIMARY KEY,
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

db.con.commit()
