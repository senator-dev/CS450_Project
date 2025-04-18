import os
import psycopg
import pandas as pd


def get_data(q):
    with psycopg.connect(
        host="172.31.23.201",
        port=5434,
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"]
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(q)
            rows = cur.fetchall()
            colnames = [desc[0] for desc in cur.description]

        return pd.DataFrame(rows, columns=colnames)
