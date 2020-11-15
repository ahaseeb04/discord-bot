import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError
import psycopg2 

from bot import config

def connect():
    link = config.postgres_url or 'postgresql://{user}:{password}@{host}:{port}/{database}'.format(**config.postgres)
    return create_engine(link)

def _csv_to_sql(engine, table):
    df = pd.read_csv('postgres/support/aliases.csv')
    df.to_sql(table, engine, if_exists='replace', index=False )

def sql_to_df(engine, table, index):
    try:
        return pd.read_sql(table, engine).set_index(index)
    except ProgrammingError:
        _csv_to_sql(engine, table)
        return sql_to_df(engine, table, index)

def df_to_sql(df, engine, table):
    df.to_sql(table, engine, if_exists='replace')

def df_to_dict(df):
    return df.to_dict()

if __name__ == "__main__":
    eng = connect()
    df = sql_to_df(eng, 'aliases', 'alias')
    print(df.to_string())