import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.engine.url import URL
import psycopg2 

from bot import config

def engine():
    link = config.database_url or URL(**config.database)
    return create_engine(link)

def _csv_to_sql(table, engine):
    df = pd.read_csv(f'database/support/{table}.csv')
    df.to_sql(table, engine, if_exists='replace')

def _sql_to_csv(table, engine):
    df = pd.read_sql(table, engine)
    df.to_csv(f'database/support/{table}.csv', index=False)

def sql_to_df(table, engine, index):
    try:
        return pd.read_sql(table, engine).set_index(index)
    except ProgrammingError:
        _csv_to_sql(table, engine)
        return sql_to_df(table, engine, index)

def df_to_sql(df, table, engine):
    df.to_sql(table, engine, if_exists='replace')

def df_to_dict(df):
    return df.to_dict()
