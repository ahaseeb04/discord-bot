from pytz import timezone
from datetime import date, datetime

from tabulate import tabulate
from discord.ext import commands
import aiocron

from database_tools import engine, sql_to_df, df_to_sql
from bot import config
from ._cog import _Cog

import pandas as pd
import redis

class Unverify(_Cog):
    def __init__(self, client):
        _Cog.__init__(self, client)
        tz = timezone('US/Eastern')
        self.redis = redis.StrictRedis.from_url(config.redis_url, decode_responses=True)
        self.engine = engine(db_url=config.postgres_url, db_params=config.postgres_params)
        self.df = sql_to_df('last message', self.engine, 'user id')
        aiocron.crontab('0 4 * * *', func=self.push_df, tz=tz)

    @_Cog.listener(name='on_message')
    async def unverify(self, message):
        if any(str(role.id) == config.verified_role for role in message.author.roles):
            self.redis.hmset("users" , {message.author.id : date.today().isoformat()})

    async def push_df(self):
        data = self.redis.hgetall("users")
        df = pd.DataFrame.from_dict(data, orient='index', columns=['date']).rename_axis('user id')
        df = pd.concat([self.df, df]).groupby(level=0).last()
        df_to_sql(df, 'last message', self.engine)
        self.redis.delete('users')
        print(df)

    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def get_df(self, context):
        self.df = sql_to_df('last message', self.engine, 'user id')
        await context.channel.send(f"```\n{tabulate(self.df, headers='keys', tablefmt='psql')}```")
    
    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def get_redis(self, context):
        data = self.redis.hgetall("users")
        df = pd.DataFrame.from_dict(data, orient='index', columns=['date']).rename_axis('user id')
        await context.channel.send(f"```\n{tabulate(df, headers='keys', tablefmt='psql')}```")

    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def clear_redis(self, context):
        self.redis.delete('users')

    