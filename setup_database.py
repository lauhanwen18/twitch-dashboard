"""
Initialize the SQLite database using schema.sql
Run with: python3 setup_database.py
"""

import sqlite3

DB_PATH = "twitch_data.db"
SCHEMA_PATH = "schema.sql"

def main():
    with open(SCHEMA_PATH, "r") as f:
        schema_sql = f.read()

    conn = sqlite3.connect(DB_PATH)
    conn.executescript(schema_sql)
    conn.commit()
    conn.close()

    print(f"Database initialized at {DB_PATH}")

if __name__ == "__main__":
    main()