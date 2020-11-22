from pytz import timezone
from datetime import date, datetime
import os

# from tabulate import tabulate
from discord.ext import commands
import aiocron
import pandas as pd
import redis

from database_tools import engine, sql_to_df, df_to_sql, redis_access
from bot import config
from ._cog import _Cog

class LastMessage(_Cog):
    def __init__(self, client):
        _Cog.__init__(self, client)
        tz = timezone('US/Eastern')
        self.redis = redis_access(url=config.redis_url, params=config.redis_params)
        self.engine = engine(url=config.postgres_url, params=config.postgres_params)
        self.df = sql_to_df('last message', self.engine, 'user id')
        aiocron.crontab('0 3 * * * ', func=self.cronjobs, tz=tz)

    @_Cog.listener()
    async def on_message(self, message):
        author = message.guild.get_member(message.author.id)
        if author is not None and any(str(role.id) == config.verified_role for role in author.roles):
            self.redis.hmset("users" , {message.author.id : date.today().isoformat()})

    async def cronjobs(self):
        self.df = await self.backup_redis()
        self.df = await self.check_verified()
        df_to_sql(self.df, 'last message', self.engine)

    # @commands.has_permissions(manage_roles=True)
    # @commands.command(hidden=True)
    # async def set_redis(self, context):
    #     await self.backup_redis()

    async def backup_redis(self):
        data = self.redis.hgetall("users")
        df = pd.DataFrame.from_dict(data, orient='index', columns=['last message']).rename_axis('user id')
        df = pd.concat([self.df, df]).groupby(level=0).last()
        self.redis.delete('users')
        return df

    # @commands.has_permissions(manage_roles=True)
    # @commands.command(hidden=True)
    # async def verifid(self, context):
    #     await self.check_verified()

    async def check_verified(self):
        data = {}
        for user in self.client.get_all_members():
            if any(str(role.id) == config.verified_role for role in user.roles):
                data[str(user.id)] = [date.today().isoformat(), float('nan')]
        df = pd.DataFrame.from_dict(data, orient='index', columns=['verified', 'last message']).rename_axis('user id')
        df.update(self.df)
        return df.dropna(how="any", subset=['verified'])

    @commands.has_permissions(manage_roles=True)
    @commands.command(hidden=True)
    async def users(self, context):
        await self.deverify_users()

    async def deverify_users(self):
        get_date = lambda row: datetime.strptime(row['last message'] or row['verified'], "%Y-%m-%d").date()
        self.df['days'] = self.df.apply((lambda row: (date.today() - get_date(row)).days), axis=1)

        guild = self.client.get_guild(int(config.server_id))
        role = guild.get_role(int(config.verified_role))
        for id in self.df.loc[self.df['days'] >= config.deverify_days].index:
            await guild.get_member(int(id)).remove_roles(role)

    @commands.has_permissions(manage_roles=True)
    @commands.command(hidden=True)
    async def days(self, context):
        print(config.deverify_days)

    @commands.has_permissions(manage_roles=True)
    @commands.command(hidden=True)
    async def set_days(self, context):
        days = context.message.content.split()[1]
        os.system(f'heroku config:set DEVERIFY_DAYS={days}')
        # with open('.env') as e:
        #     print(e)
        # os.environ['DEVERIFY_DAYS'] = days
        # print(os.environ['DEVERIFY_DAYS'])
        # print(config.deverify_days)


    # @commands.has_permissions(manage_roles=True)
    # @commands.command(hidden=True)
    # async def get_df(self, context):
    #     self.df = sql_to_df('last message', self.engine, 'user id')
    #     print(self.df)
    #     await context.channel.send(f"```\n{tabulate(self.df, headers='keys', tablefmt='psql')}```")
    
    # @commands.has_permissions(manage_roles=True)
    # @commands.command(hidden=True)
    # async def get_redis(self, context):
    #     data = self.redis.hgetall("users")
    #     df = pd.DataFrame.from_dict(data, orient='index', columns=['last message']).rename_axis('user id')
    #     print(df)
    #     await context.channel.send(f"```\n{tabulate(df, headers='keys', tablefmt='psql')}```")



    