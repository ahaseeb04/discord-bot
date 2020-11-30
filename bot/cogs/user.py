from discord.ext import commands
from disputils import BotEmbedPaginator

from bot.utils import get_user
from bot.exceptions import DataNotFoundError
from ._cog import _Cog

class User(_Cog, name="user"):
    @commands.command(brief='Fetch details for a spcified user.', aliases=['member', 'u', 'whois'])
    async def user(self, context):
        try:
            embeds = [await get_user(context, user) for user in context.message.mentions]
            if not len(embeds):
                raise DataNotFoundError()
            
        except DataNotFoundError:
            await context.message.channel.send('**Error**: Sorry, please specify a valid user.')
        else:
            await BotEmbedPaginator(context, embeds).run()

    @commands.command(brief='Fetch details about yourself.')
    async def me(self, context):
        await context.message.channel.send(embed=await get_user(context, context.message.author))

