import re
from itertools import tee

import discord
from discord.ext import commands

from scrapers import scrape_course_list
from bot.embed_builder import EmbedBuilder
from ._cog import _Cog

class CourseList(_Cog, name="course list"):
    @commands.command(brief='Fetch all the courses for a specified program.')
    async def courselist(self, context):
        error = "The requested course list was not found. \n\
            \nCourse lits should be of the form: \
            \n\u2003\u2002[faculty] dept [session year] \n\
            \nExamples: \
            \n\u2003\u2022 EECS \
            \n\u2003\u2022 LE EECS  \
            \n\u2003\u2022 EECS FW 2020 \
            \n\u2003\u2022 LE EECS FW 2020"

        courses = ' '.join(context.message.content.split()[1:])
        info = re.match("".join((
            "^(?:(?P<faculty>[a-z]{2})\s)?"
            "(?:(?P<department>[a-z]{2,4}))+"
            "(?:\s(?P<session>[a-z]{2})\s?(?P<year>[0-9]{4}))?$"
        )), courses.lower())

        try:
            course_list, test = tee(scrape_course_list(info.groupdict()))

            if next(test, None) is None:
                raise Exception()
            else:
                embeds = EmbedBuilder(max_fields=24)
                for course in course_list:
                    embeds.add_field(name=course[0], value=f'[{course[1]}]({course[2]})')
                for embed in embeds:
                    await context.channel.send(embed=embed)
        except Exception:
            embed = discord.Embed(title="Error", description=error, color=0xff0000, inline=False)
            await context.channel.send(embed=embed)
