import re
from itertools import tee

import discord
from discord.ext import commands
from disputils import BotEmbedPaginator

from ._cog import _Cog
from scrapers import scrape_course_list
from bot.regex import course_list_regex
from bot.errors import course_list_error
from bot.embed_builder import EmbedBuilder
from bot.exceptions import DataNotFoundError, IllegalFormatError

class CourseList(_Cog, name='course'):
    @commands.command(brief='Fetch all the courses for a specified program.')
    async def courselist(self, context):
        course_list = ' '.join(context.message.content.split()[1:])
        info = re.match(course_list_regex, course_list.lower())

        try:
            if info is None:
                raise IllegalFormatError()

            course_list, test = tee(scrape_course_list(info.groupdict()))

            if next(test, None) is None:
                raise DataNotFoundError()

        except (DataNotFoundError, IllegalFormatError):
            embed = discord.Embed(title="Error", description=course_list_error, color=0xff0000, inline=False)
            await context.channel.send(embed=embed)
        else:
            embeds = EmbedBuilder(max_fields=24)
            for course in course_list:
                embeds.add_field(name=course[0], value=f'[{course[1]}]({course[2]})')

            await BotEmbedPaginator(context, list(embeds)).run()
