import re
from itertools import tee

import discord
from discord.ext import commands

from scrapers import scrape_course_list
from bot.exceptions import DataNotFoundException, IllegalFormatException
from bot.errors import course_list_error
from bot.regex import course_list_regex
from bot.embed_builder import EmbedBuilder
from ._cog import _Cog

class CourseList(_Cog, name="course list"):
    @commands.command(brief='Fetch all the courses for a specified program.')
    async def courselist(self, context):
        course_list = ' '.join(context.message.content.split()[1:])
        info = re.match(course_list_regex, course_list.lower())

        try:
            if info is None:
                raise IllegalFormatException()

            course_list, test = tee(scrape_course_list(info.groupdict()))
            if next(test, None) is None:
                raise DataNotFoundException()

            embeds = EmbedBuilder(max_fields=24)
            for course in course_list:
                embeds.add_field(name=course[0], value=f'[{course[1]}]({course[2]})')

            for embed in embeds:
                await context.channel.send(embed=embed)    
        except (DataNotFoundException, IllegalFormatException):
            embed = discord.Embed(title="Error", description=course_list_error, color=0xff0000, inline=False)
            await context.channel.send(embed=embed)
