import psycopg2
import pandas as pd


def fetch_postgres_data(table_name):
    conn = psycopg2.connect(
        host="localhost",
        user="your_pg_user",
        password="your_password",
        dbname="your_pg_db"
    )
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df.to_dict(orient="records")
