from discord.ext import commands
from disputils import BotEmbedPaginator

from ._cog import _Cog
from bot.utils import get_user

class User(_Cog, name="user"):
    @commands.command(brief='Fetch details for a user.', aliases=['member', 'u', 'whois'])
    async def user(self, context):
        embeds = [ get_user(context, user) for user in context.message.mentions ]

        if not len(embeds):
            await context.message.channel.send(embed=get_user(context, context.message.author))
        else:
            await BotEmbedPaginator(context, embeds).run()
