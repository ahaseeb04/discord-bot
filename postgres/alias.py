# import pandas as pd

def set_alias(df, alias, role=None):
    return set_unalias(df, alias).append({
        'alias': alias,
        'role': role
    }, ignore_index=True)

def set_unalias(df, alias):
    return df[df.alias != alias].reset_index(drop=True)