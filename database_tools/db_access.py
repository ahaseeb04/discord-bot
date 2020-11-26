import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.engine.url import URL
import psycopg2 

def engine(url=None, params=None):
    return create_engine(url or URL(**params))

def _csv_to_sql(table, engine, index):
    df = pd.read_csv(f'database_tools/support/{table}.csv').set_index(index)
    df.to_sql(table, engine, if_exists='replace')

def _sql_to_csv(table, engine):
    df = pd.read_sql(table, engine)
    df.to_csv(f'database_tools/support/{table}.csv', index=False)

def sql_to_df(table, engine, index):
    if not engine.dialect.has_table(engine, table):
        _csv_to_sql(table, engine, index)
    return pd.read_sql(table, engine).set_index(index)

def df_to_sql(df, table, engine):
    df.to_sql(table, engine, if_exists='replace')

def df_to_dict(df):
    return df.to_dict()

def dict_to_df(data, index):
    return pd.DataFrame.from_dict(data).rename_axis(index)
