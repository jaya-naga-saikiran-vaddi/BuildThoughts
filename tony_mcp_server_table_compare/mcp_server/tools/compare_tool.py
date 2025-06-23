import pandas as pd


def compare_tables(mysql_data, pg_data):
    df_mysql = pd.DataFrame(mysql_data)
    df_pg = pd.DataFrame(pg_data)

    common_cols = list(set(df_mysql.columns).intersection(set(df_pg.columns)))

    if not common_cols:
        return [{"error": "No common columns to compare"}]

    merged = df_mysql.merge(df_pg, on=common_cols, suffixes=("_mysql", "_pg"), how="outer", indicator=True)
    differences = merged[merged["_merge"] != "both"]

    return differences.to_dict(orient='records')
