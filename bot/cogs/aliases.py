from tabulate import tabulate

import discord
from discord.ext import commands

from bot.exceptions import InvalidPermissionsError, WrongChannelError, IllegalFormatError, DataNotFoundError
from postgres import set_alias, set_unalias, connect, sql_to_df, df_to_sql
from ._cog import _Cog

class Aliases(_Cog, name='aliases'):
    def __init__(self, client):
        _Cog.__init__(self, client)
        self.engine = connect()
        self.df = sql_to_df(self.engine)

    @commands.command(brief="Get a List of aliases")
    async def aliases(self, context):
        try:
            if not context.message.author.guild_permissions.manage_roles:
                raise InvalidPermissionsError()
        except InvalidPermissionsError:
            await context.channel.send("Insufficient permissions")
        else:
            await context.channel.send(f"```\n{tabulate(self.df, headers='keys', tablefmt='psql')}```")

    @commands.command(brief="Add/Update alias")
    async def alias(self, context):
        try:
            if not context.message.author.guild_permissions.manage_roles:
                raise InvalidPermissionsError()

            data = {i : val.strip() for i, val in enumerate(context.message.content.split(self.client.command_prefix)[2:4])}
            if not len(data):
                raise IllegalFormatError()
            alias, role = data.get(0).lower(), data.get(1)

            self.df = set_alias(self.df, alias, role)
        except InvalidPermissionsError:
            await context.channel.send("Insufficient permissions")
        except IllegalFormatError:
            await context.channel.send('No alias provided')
        else:
            await context.channel.send(f'Role "{alias}" has been set to "{role}"')
            df_to_sql(self.df, self.engine)

    @commands.command(brief="Remove alias")
    async def unalias(self, context):
        try:
            if not context.message.author.guild_permissions.manage_roles:
                raise InvalidPermissionsError()

            data = context.message.content.split(self.client.command_prefix)[2:3]
            if not len(data):
                raise IllegalFormatError()
            alias = data[0].strip().lower()

            if alias not in self.df.index:
                raise DataNotFoundError()

            self.df = set_unalias(self.df, alias)
        except InvalidPermissionsError:
            await context.channel.send("Insufficient permissions")
        except IllegalFormatError:
            await context.channel.send('No alias provided')
        except DataNotFoundError:
            await context.channel.send(f'Alias "{alias}" does not exist')
        else:
            await context.channel.send(f'Role "{alias}" has been removed')
            df_to_sql(self.df, self.engine)
