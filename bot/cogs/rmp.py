import discord
from itertools import tee
from discord.ext import commands
from disputils import BotEmbedPaginator

from ._cog import _Cog
from scrapers import scrape_rmp
from bot.exceptions import DataNotFoundError

class RMP(_Cog, name='rmp'):
    @commands.command(brief="Fetch a professor's information from RateMyProfessors.", aliases=['prof', 'professor'])
    async def rmp(self, context):
        professor_name = context.message.content.lower().split()[1:]

        def _build_embed(professor):
            embed = discord.Embed(title=professor['name'], description=professor['department'], url=professor['url'], color=0x1d4ed8)
            embed.set_thumbnail(url='https://i.imgur.com/dwlne0a.png')

            if professor['top_review'] is not None:
                embed.add_field(name='Top review', value=professor['top_review'], inline=False)
            if professor['rating'] != 'N/A':
                count = professor['based_on_count']
                count_formatted = count + ' review' if count == '1' else count + ' reviews'
                text = professor['rating'] + '/5' + ' (based on ' + count_formatted + ')'
                embed.add_field(name='Rating', value=text, inline=False)
            for label, rating in professor['feedback']:
                text = rating if '%' in rating else rating + '/5'
                embed.add_field(name=label, value=text, inline=False)

            return embed

        try:
            professors, test = tee(scrape_rmp(professor_name))

            if next(test, None) is None:
                raise DataNotFoundError()
        except DataNotFoundError:
            await context.message.channel.send('**Error**: Sorry, could not find professor!')
        else:
            embeds = [ _build_embed(professor) for professor in professors ]
            await BotEmbedPaginator(context, embeds).run()
