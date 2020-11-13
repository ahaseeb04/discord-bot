import pandas as pd
from sqlalchemy import create_engine

from bot import config

def connect():
    link = 'postgresql://{user}:{password}@{host}:{port}/{database}'.format(**config.postgres)
    return create_engine(link)

def _csv_to_sql(engine):
    df = pd.read_csv('bot/support/aliases.csv')
    df.to_sql('aliases', engine, if_exists='replace', index=False )

def sql_to_df(engine):
    return pd.read_sql('aliases', engine)

def df_to_sql(df, engine):
    df.to_sql('aliases', engine, if_exists='replace')

if __name__ == "__main__":
    eng = connect()
    df = sql_to_df(eng)
    print(df)