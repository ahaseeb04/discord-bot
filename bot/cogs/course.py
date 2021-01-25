import re
import csv
from datetime import datetime, timedelta

import discord
from discord.ext import commands
from disputils import BotEmbedPaginator

from ._cog import _Cog
from scrapers import scrape_course
from bot.errors import course_error
from bot.regex import course_regex
from bot.embed_builder import EmbedBuilder
from bot.exceptions import DataNotFoundError, IllegalFormatError

class Course(_Cog, name="course"):
    @commands.command(brief='Fetch information regarding a course from YorkU.', aliases=['c'])
    async def course(self, context):
        def _format_course(course_info):
            embeds = EmbedBuilder(
                title=course_info['heading'],
                description=course_info['description'],
                color=0x047857,
                url=course_info['url'],
                thumbnail='http://continue.yorku.ca/york-scs/wp-content/uploads/2016/06/YorkU-logo6.jpg',
                store=False
            )
            for section in course_info['sections']:
                tmp = EmbedBuilder()
                tmp.add_field(name='\u200b', value=f"___***{section['section_info']}***___", inline=False)
                for name, value in _format_section(section):
                    tmp.add_field(name=name, value=value, inline=False)
                if len(tmp.get_fields()) > 1:
                    embeds.insert_embed(tmp)
            if len(embeds.get_fields()) == 0:
                tmp = EmbedBuilder()
                tmp.add_field(
                    name="No Sections Found",
                    value="**This course listing may be a duplicate. There may be other listings with valid sections.*"
                )
                embeds.insert_embed(tmp)
            return embeds

        def _format_section(section):
            def _format_lectures(lectures):
                for lecture in lectures:
                    yield ' '.join(_format_lecture(lecture))

            def _format_catalogue(catalogue):
                return f"Cat #: {''.join(catalogue)}" if catalogue else ''

            def _format_lecture(lecture):
                def _format_day(day):
                    return dict(csv.reader(open('bot/support/days.csv', 'r'))).get(day, '')

                def _format_times(time, duration):
                    def _format_time(time):
                        return datetime.strptime(str(time), "%H:%M:%S").strftime('%-I:%M %p')

                    if duration == '0':
                        return 'No Scheduled Time'

                    hours, minutes = map(int, time.split(':'))
                    start = timedelta(hours=hours, minutes=minutes)
                    end = start + timedelta(minutes=int(duration))

                    return f'{_format_time(start)} to {_format_time(end)}'

                def _format_location(location):
                    return f'@{location}' if location != '\xa0 ' else ''

                def _format_backup(backup):
                    return f' ({backup})' if backup is not None else ''

                yield _format_day(lecture['day'])
                yield _format_times(lecture['start time'], lecture['duration'])
                yield _format_location(lecture['location'])
                yield _format_backup(lecture.get('backup'))

            for name, lecture in section['lectures'].items():
                if len(lecture['lecture_info']) > 0:
                    yield (
                        f"{name}: {lecture['instructors'] or 'Not Available'}",
                        '\n'.join((
                            _format_catalogue(lecture['catalogue_numbers']),
                            '\n'.join(_format_lectures(lecture['lecture_info']))
                        ))
                    )


        course = ' '.join(context.message.content.split()[1:])
        info = re.match(course_regex, course.lower())

        try:
            if info is None:
                raise IllegalFormatError()

            courses = scrape_course(info.groupdict())
            embeds = [ embed for course_info in courses for embed in _format_course(course_info) ]

            if not len(embeds):
                raise DataNotFoundError()

        except (DataNotFoundError, IllegalFormatError):
            embed = discord.Embed(title="Error", description=course_error, color=0xff0000, inline=False)
            await context.channel.send(embed=embed)
        else:
            await BotEmbedPaginator(context, embeds).run()
