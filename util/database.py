import sqlite3

DB_FILE = "Info.db"
db = sqlite3.connect(DB_FILE)
c = db.cursor()
