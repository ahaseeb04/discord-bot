from discord.ext import commands

from bot.utils import get_user
from ._cog import _Cog

class User(_Cog, name="user"):
    @commands.command(brief='Fetch details for a user.', aliases=['member', 'u', 'whois'])
    async def user(self, context):
        for user in context.message.mentions:
            await get_user(context, user)
