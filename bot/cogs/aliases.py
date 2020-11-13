from tabulate import tabulate

import discord
from discord.ext import commands

from bot.exceptions import InvalidPermissionsError, WrongchannelError
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
            # await context.channel.send(f"```{self.df.reset_index().to_string(index=False)}```")
            await context.channel.send(f"```\n{tabulate(self.df.sort_values(by=['alias']), headers='keys', tablefmt='psql')}```")

    @commands.command(brief="Add/Update alias")
    async def alias(self, context):
        try:
            if not context.message.author.guild_permissions.manage_roles:
                raise InvalidPermissionsError()

            vals = [val.strip() for val in context.message.content.split(self.client.command_prefix)]
            alias, role = vals[2], get_index(vals, 3)
        except IndexError:
            await context.channel.send('No alias provided')
        except InvalidPermissionsError:
            await context.channel.send("Insufficient permissions")
        else:
            self.df = set_alias(self.df, alias, role)
            await context.channel.send(f'Role "{alias}" has been set to "{role}"')
            df_to_sql(self.df, self.engine)

    @commands.command(brief="Remove alias")
    async def unalias(self, context):
        try:
            if not context.message.author.guild_permissions.manage_roles:
                raise InvalidPermissionsError()

            alias = [val.strip() for val in context.message.content.split(self.client.command_prefix)][2]
            self.df = set_unalias(self.df, alias)
        except IndexError:
            await context.channel.send('No alias provided')
        except KeyError:
            await context.channel.send(f'Alias "{alias}" does not exist')
        except InvalidPermissionsError:
            await context.channel.send("Insufficient permissions")
        else:
            await context.channel.send(f'Role "{alias}" has been removed')
            df_to_sql(self.df, self.engine)

def get_index(lst, i, default=None):
    try:
        return lst[i]
    except IndexError:
        return default

