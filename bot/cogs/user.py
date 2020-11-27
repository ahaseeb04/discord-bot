from discord.ext import commands
from disputils import BotEmbedPaginator

from bot.utils import get_user
from bot.exceptions import DataNotFoundError, IllegalFormatError
from ._cog import _Cog

class User(_Cog, name="user"):
    @commands.command(brief='Fetch details for a user.', aliases=['member', 'u', 'whois'])
    async def user(self, context):
        try:
            if not len(context.message.raw_mentions) \
                and not len(context.message.channel_mentions)\
                and not len(context.message.role_mentions):
                    raise IllegalFormatError()

            if not len(context.message.mentions):
                raise DataNotFoundError()
            
            embeds = [get_user(context, user) for user in context.message.mentions]

        except IllegalFormatError:
            await context.message.channel.send(embed=get_user(context, context.message.author))
        except DataNotFoundError:
            await context.message.channel.send('**Error**: Sorry, could not find user!')
        else:
            await BotEmbedPaginator(context, embeds).run()