from pytz import timezone
from datetime import date, datetime
import os

from tabulate import tabulate
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
        self.df = sql_to_df('last_message', self.engine, 'user_id')
        self.deverify_days = sql_to_df('deverify_days', self.engine, 'index')
        aiocron.crontab('0 3 * * *', func=self.cronjobs, tz=tz)

    @_Cog.listener()
    async def on_message(self, message):
        guild = self.client.get_guild(int(config.server_id))
        author = guild.get_member(message.author.id)
        if author is not None and any(str(role.id) == config.verified_role for role in author.roles):
            self.redis.hmset("users" , {message.author.id : date.today().isoformat()})

    # @commands.has_permissions(manage_roles=True)
    # @commands.command(hidden=True)
    # async def run_crons(self, context):
    #     await self.cronjobs()

    async def cronjobs(self):
        self.df = await self.backup_redis()
        self.df = await self.check_verified()
        await self.deverify_users()
        self.df = await self.check_verified()
        df_to_sql(self.df, 'last_message', self.engine)

    # @commands.has_permissions(manage_roles=True)
    # @commands.command(hidden=True)
    # async def backup(self, context):
    #     await self.backup_redis()

    async def backup_redis(self):
        data = self.redis.hgetall("users")
        df = pd.DataFrame.from_dict(data, orient='index', columns=['last_message']).rename_axis('user_id')
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
                data[str(user.id)] = [date.today().isoformat(), None]
        df = pd.DataFrame.from_dict(data, orient='index', columns=['verified','last_message']).rename_axis('user_id')
        df.update(self.df)
        return df.dropna(how="any", subset=['verified'])

    # @commands.has_permissions(manage_roles=True)
    # @commands.command(hidden=True)
    # async def deverify(self, context):
    #     await self.deverify_users()

    async def deverify_users(self):
        get_date = lambda row: datetime.strptime(max(row['last_message'] or '0', row['verified']), "%Y-%m-%d").date()
        self.df['days'] = self.df.apply((lambda row: (date.today() - get_date(row)).days), axis=1)

        guild = self.client.get_guild(int(config.server_id))
        role = guild.get_role(int(config.verified_role))
        for id in self.df.loc[self.df['days'] >= int(self.deverify_days.iloc[0].days)].index:
            await guild.get_member(int(id)).remove_roles(role)

    @commands.has_permissions(manage_guild=True)
    @commands.command(aliases=['get_dever'])
    async def deverification_days(self, context):
        await context.message.channel.send(f'User de-verification is set to {self.deverify_days.at[0, "days"]} days.')

    @commands.has_permissions(manage_guild=True)
    @commands.command(aliases=['set_dever'])
    async def set_deverification_days(self, context):
        days = context.message.content.split()
        if len(days) > 1:
            self.deverify_days.at[0, 'days'] = days[1]
            df_to_sql(self.deverify_days, 'deverify_days', self.engine)
            await context.message.channel.send(f'Users de-verification has been set to {days[1]} days.')
        else:
            await context.message.channel.send('**Error**: Must specify number of days')

    # @commands.has_permissions(manage_roles=True)
    # @commands.command(hidden=True)
    # async def get_df(self, context):
    #     self.df = sql_to_df('last_message', self.engine, 'user_id')
    #     await context.channel.send(f"```\n{tabulate(self.df, headers='keys', tablefmt='psql')}```")
    
    # @commands.has_permissions(manage_roles=True)
    # @commands.command(hidden=True)
    # async def get_redis(self, context):
    #     data = self.redis.hgetall("users")
    #     df = pd.DataFrame.from_dict(data, orient='index', columns=['last_message']).rename_axis('user_id')
    #     await context.channel.send(f"```\n{tabulate(df, headers='keys', tablefmt='psql')}```")


    