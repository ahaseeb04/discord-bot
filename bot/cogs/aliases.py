from tabulate import tabulate

import discord
from discord.ext import commands

from bot import config
from bot.exceptions import WrongChannelError, IllegalFormatError, DataNotFoundError
from database_tools import set_alias, set_unalias, engine, sql_to_df, df_to_sql
from ._cog import _Cog

class Aliases(_Cog, name='aliases'):
    def __init__(self, client):
        _Cog.__init__(self, client)
        self.engine = engine()
        self.df = sql_to_df('aliases', self.engine, 'alias')

    @commands.has_permissions(manage_guild=True)
    @commands.command(brief="Get a List of aliases")
    async def aliases(self, context):
        await context.channel.send(f"```\n{tabulate(self.df, headers='keys', tablefmt='psql')}```")

    @commands.has_permissions(manage_guild=True)
    @commands.command(brief="Add/Update alias")
    async def alias(self, context):
        try:
            data = {i : val.strip() for i, val in enumerate(context.message.content.split(self.client.command_prefix)[2:4])}
            if not len(data):
                raise IllegalFormatError()
            alias, role = data.get(0).lower(), data.get(1)

            self.df = set_alias(self.df, alias, role)
        except IllegalFormatError:
            await context.channel.send('No alias provided')
        else:
            await context.channel.send(f'Role "{alias}" has been set to "{role}"')
            df_to_sql(self.df, 'aliases', self.engine)

    @commands.has_permissions(manage_guild=True)
    @commands.command(brief="Remove alias")
    async def unalias(self, context):
        try:
            data = context.message.content.split(self.client.command_prefix)[2:3]
            if not len(data):
                raise IllegalFormatError()
            alias = data[0].strip().lower()

            if alias not in self.df.index:
                raise DataNotFoundError()

            self.df = set_unalias(self.df, alias)
        except IllegalFormatError:
            await context.channel.send('No alias provided')
        except DataNotFoundError:
            await context.channel.send(f'Alias "{alias}" does not exist')
        else:
            await context.channel.send(f'Role "{alias}" has been removed')
            df_to_sql(self.df, 'aliases', self.engine)
