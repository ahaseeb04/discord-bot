import pandas as pd

def set_alias(df, alias, role=None):
    df.at[alias, 'role'] = role
    return df

def set_unalias(df, alias):
    return df.drop(alias)
