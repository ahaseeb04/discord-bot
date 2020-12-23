import discord
from discord.ext import commands

from ._cog import _Cog

class Nuke(_Cog):
    @commands.command(brief='Nuke your message history.', hidden=True)
    async def nuke(self, context):
        abdul = 364856110806728707

        if context.message.author.id == abdul:
            await context.message.delete()
            await context.channel.purge(limit=20000, check=lambda message: message.author.id == abdul)
        else:
            await context.channel.send('This command can only be used by Abdul!')
