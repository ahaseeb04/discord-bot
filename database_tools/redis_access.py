import pandas as pd
import redis

def redis_access(url=None, params=None):
    if url:
        return redis.StrictRedis.from_url(url, decode_responses=True)
    return redis.StrictRedis(decode_responses=True, db=0, **params)
