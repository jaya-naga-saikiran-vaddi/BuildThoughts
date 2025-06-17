import mysql.connector
import pandas as pd


def fetch_mysql_data(table_name):
    conn = mysql.connector.connect(
        host="localhost",
        user="your_mysql_user",
        password="your_password",
        database="your_mysql_db"
    )
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df.to_dict(orient="records")
