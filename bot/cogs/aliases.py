from tabulate import tabulate
import discord
from discord.ext import commands

from bot import config
from bot.exceptions import WrongChannelError, IllegalFormatError, DataNotFoundError
from database_tools import engine, sql_to_df, df_to_sql
from ._cog import _Cog

class Aliases(_Cog, name='aliases'):
    def __init__(self, client):
        _Cog.__init__(self, client)
        self.engine = engine(url=config.postgres_url, params=config.postgres_params)
        self.df = sql_to_df('aliases', self.engine, 'alias')

    @commands.has_permissions(manage_roles=True)
    @commands.command(brief="Get all the aliases.")
    async def aliases(self, context):
        await context.channel.send(f"```\n{tabulate(self.df, headers='keys', tablefmt='psql')}```")

    @commands.has_permissions(manage_roles=True)
    @commands.command(brief="Add or update an alias.")
    async def alias(self, context):
        try:
            data = {i : val.strip() for i, val in enumerate(context.message.content.split(self.client.command_prefix)[2:4])}
            if not len(data):
                raise IllegalFormatError()
            alias, role = data.get(0).lower(), data.get(1)

            self.df.at[alias, 'role'] = role
            self.df = self.df.sort_values(by=['alias'])
        except IllegalFormatError:
            await context.channel.send('No alias provided')
        else:
            await context.channel.send(f'Alias "{alias}" has been mapped to "{role}" role.')
            df_to_sql(self.df, 'aliases', self.engine)

    @commands.has_permissions(manage_roles=True)
    @commands.command(brief="Remove an alias.")
    async def unalias(self, context):
        try:
            data = context.message.content.split(self.client.command_prefix)[2:3]
            if not len(data):
                raise IllegalFormatError()
            alias = data[0].strip().lower()

            if alias not in self.df.index:
                raise DataNotFoundError()

            self.df = self.df.drop(alias)
        except IllegalFormatError:
            await context.channel.send('No alias provided')
        except DataNotFoundError:
            await context.channel.send(f'Alias "{alias}" does not exist')
        else:
            await context.channel.send(f'Alias "{alias}" has been removed')
            df_to_sql(self.df, 'aliases', self.engine)
