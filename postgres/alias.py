import pandas as pd

def set_alias(df, alias, role=None):
    df.at[alias, 'role'] = role
    return df.sort_values(by=['alias'])

def set_unalias(df, alias):
    return df.drop(alias)
