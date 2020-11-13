# import psycopg2
import pandas as pd
from sqlalchemy import create_engine

from bot import config

# def connect(config):
#     try:
#         connection = psycopg2.connect(**config.postgres)
#         cursor = connection.cursor()   
#         print("PostgreSQL connection is open")
#     except (Exception, psycopg2.Error) as error :
#         print ("Error while connecting to PostgreSQL", error)
#     finally:
#         return connection, cursor

# def disconnect(connection, cursor):
#     if(connection):
#         cursor.close()
#         connection.close()
#         print("PostgreSQL connection is closed")

def csv_to_sql(engine):
    df = pd.read_csv('bot/support/aliases.csv')
    df.to_sql('aliases', engine, if_exists='replace', index=False )

def sql_to_df(engine):
    return pd.read_sql('aliases', engine)

def df_to_sql(df):
    df.to_sql('aliases', engine, if_exists='replace')

def alias(df, alias, role=None):
    return unalias(df, alias).append({
        'alias': alias,
        'role': role
    }, ignore_index=True)

def unalias(df, alias):
    return df[df.alias != alias].reset_index(drop=True)


def connect():
    link = 'postgresql://{user}:{password}@{host}:{port}/{database}'.format(**config.postgres)
    return create_engine(link)


engine = connect()
df = sql_to_df(engine)
print(df)
df = alias(df, 'politics', 'gender studies')
print(df)
df = unalias(df, 'soft')
print(df)
df = alias(df, 'politics', 'poli-sci')
print(df)

 