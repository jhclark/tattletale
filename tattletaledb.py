import sqlite3
from datetime import date
import dateutil
import datetime
import configparser

def openDb(config: configparser.ConfigParser) -> (sqlite3.Connection, sqlite3.Cursor):
    dbName = config.get('database', 'dbName')
    conn = sqlite3.connect(dbName)
    cursor = conn.cursor()
    createDb(cursor)
    return (conn, cursor)

def closeDb(conn):
    conn.commit()
    conn.close()

def createDb(cursor: sqlite3.Cursor):
    # http://stackoverflow.com/questions/2614483/can-i-create-a-datetime-column-with-default-value-in-sqlite3
    cursor.execute("""CREATE TABLE IF NOT EXISTS events
        (time DATETIME PRIMARY KEY DEFAULT current_timestamp,
         location TEXT,
         isRouterUp BOOLEAN,
         isModemUp BOOLEAN,
         isInternetUp BOOLEAN);""")

def writeDbEvent(config: configparser.ConfigParser, isRouterUp: bool, isModemUp: bool, isInternetUp: bool):
    print("Doing DB insert")
    (conn, cursor) = openDb(config)
    location = config.get('location', 'location')
    cursor.execute("INSERT INTO events VALUES (datetime('now', 'localtime'), ?, ?, ?, ?);", (location, isRouterUp, isModemUp, isInternetUp))
    closeDb(conn)
    print("Did DB insert")

def getAllDbEvents(config): # -> list[(datetime, str)]:
    (conn, cursor) = openDb(config)
    cursor.execute("SELECT time, location, isRouterUp, isModemUp, isInternetUp FROM events ORDER BY date(time);")
    for row in cursor.fetchall():
        yield (dateutil.parser.parse(row[0]), row[1], row[2], row[3], row[4])
    closeDb(conn)
