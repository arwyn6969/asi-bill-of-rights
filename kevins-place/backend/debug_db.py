import sqlite3
import pandas as pd
import os

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

db_path = "kevins_place.db"

conn = sqlite3.connect(db_path)

print("--- USERS ---")
try:
    df_users = pd.read_sql_query("SELECT id, account_type, email, display_name, created_at, verified FROM users", conn)
    print(df_users)
except Exception as e:
    print(f"Error reading users: {e}")

conn.close()
