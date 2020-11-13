import discord
from discord.ext import commands

from postgres import set_alias, set_unalias, connect, sql_to_df, df_to_sql

from ._cog import _Cog

class Aliases(_Cog, name='aliases'):
    def __init__(self, client):
        _Cog.__init__(self, client)
        self.engine = connect()
        self.df = sql_to_df(self.engine)

    @commands.command(brief="Get a List of aliases")
    async def aliases(self, context):
        await context.channel.send(f"```{self.df.reset_index().to_string(index=False)}```")

    @commands.command(brief="Add/Update alias")
    async def alias(self, context):
        vals = [val.strip() for val in context.message.content.split(self.client.command_prefix)][2:4]
        self.df = set_alias(self.df, *vals)
        print(self.df)
        df_to_sql(self.df, self.engine)

    @commands.command(brief="Remove alias")
    async def unalias(self, context):
        val = [val.strip() for val in context.message.content.split(self.client.command_prefix)][2:3]
        self.df = set_unalias(self.df, *val)
        print(self.df)        
        df_to_sql(self.df, self.engine)


