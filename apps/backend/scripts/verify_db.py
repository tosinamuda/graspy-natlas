import sqlite3
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine

try:
    conn = sqlite3.connect("data/sqlite.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM interaction_logs ORDER BY id DESC LIMIT 1;")
    row = cursor.fetchone()
    if row:
        print(f"Log Found: ID={row[0]}, Type={row[1]}, UserInput={row[4]}")
        sys.exit(0)
    else:
        print("No logs found.")
        sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
finally:
    if conn:
        conn.close()
