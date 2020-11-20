import discord
from itertools import tee
from discord.ext import commands
from disputils import BotEmbedPaginator

from ._cog import _Cog
from scrapers import scrape_rmp
from bot.exceptions import DataNotFoundError

class RMP(_Cog, name='rmp'):
    @commands.command(brief="Fetch a professor's information from RateMyProfessors.", aliases=['prof'])
    async def rmp(self, context):
        professor_name = context.message.content.lower().split()[1:]

        try:
            professors, c = tee(scrape_rmp(professor_name))

            if next(c, None) is None:
                raise DataNotFoundError()
        except DataNotFoundError:
            await context.message.channel.send('**Error**: Sorry, could not find professor!')
        else:
            embeds = []

            for professor in professors:
                embed = discord.Embed(title=professor['name'], description=professor['description'], url=professor['url'], color=0x1d4ed8)
                embed.set_thumbnail(url='https://i.imgur.com/dwlne0a.png')

                embed.add_field(name='Top review', value=professor['top_review'], inline=False)
                embed.add_field(name='Rating', value=professor['rating'] + '/5', inline=False)
                embed.add_field(name='Difficulty', value=professor['difficulty'] + '/5', inline=False)
                embed.add_field(name='Retake percentage', value=professor['retake_percentage'], inline=False)

                embeds.append(embed)

            await BotEmbedPaginator(context, embeds).run()
