import pandas as pd
from sqlalchemy import create_engine

from bot import config

def connect():
    if config.postgres_url is not None:
        link = 'postgres://knbupvveehgwmn:c0274b321f56df3dbefbc9b73b26ba0a1f83e2802a698320d72ea18791dd5dc1@ec2-34-237-236-32.compute-1.amazonaws.com:5432/da806jll9l7qs6'
    else:
        link = 'postgresql://{user}:{password}@{host}:{port}/{database}'.format(**config.postgres)
    link = 'postgres://knbupvveehgwmn:c0274b321f56df3dbefbc9b73b26ba0a1f83e2802a698320d72ea18791dd5dc1@ec2-34-237-236-32.compute-1.amazonaws.com:5432/da806jll9l7qs6'
    return create_engine(link)

def _csv_to_sql(engine):
    df = pd.read_csv('bot/support/aliases.csv')
    df.to_sql('aliases', engine, if_exists='replace', index=False )

def sql_to_df(engine):
    return pd.read_sql('aliases', engine).set_index('alias')

def df_to_sql(df, engine):
    df.to_sql('aliases', engine, if_exists='replace')

def df_to_dict(df):
    return df.to_dict()

if __name__ == "__main__":
    eng = connect()
    df = sql_to_df(eng)
    print(df.to_string())