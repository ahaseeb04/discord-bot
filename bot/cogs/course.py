import re
import csv
from datetime import datetime, timedelta

import discord
from discord.ext import commands

from scrapers import scrape_course
import config


class EmbedBuilder():
    def __init__(self, **kwargs):
        self.properties = {
            'color' : kwargs.get('color', ''),
            'title' : kwargs.get('title', ''),
            'url' : kwargs.get('url', ''),
        }
        self.thumbnail = kwargs.pop('thumbnail', discord.Embed.Empty)
        self.embeds = [discord.Embed(**kwargs).set_thumbnail(url=self.thumbnail)]

    def add_field(self, **kwargs):
        embed = self.embeds[-1]
        if len(embed.fields) == 25:
            embed = discord.Embed(**self.properties).set_thumbnail(url=self.thumbnail)
            self.embeds.append(embed)
        embed.add_field(**kwargs)

    def __iter__(self):
        return iter(self.embeds)

class Course(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def course(self, context):
        def _format_output(info):
            if info.get('error', None) is not None:
                return EmbedBuilder(title="Error", description=error, color=0xff0000, inline=False)
            else:
                if sum([len(section[section_info][lecture]['lectures']) 
                    for section in info['sections'] 
                    for section_info in section 
                    for lecture in section[section_info]
                ]) > 0:
                    embeds = EmbedBuilder(
                        title=info['heading'], 
                        description=info['description'],
                        color=0x0000ff, 
                        url=info['url'],
                        thumbnail='http://continue.yorku.ca/york-scs/wp-content/uploads/2016/06/YorkU-logo6.jpg'
                    )
                    for section in info['sections']:
                        for section_info in section:
                            if sum([len(x) for l in section[section_info] for x in section[section_info][l]['lectures']]) > 0:
                                embeds.add_field(name='\u200b', value=f'___***{section_info}***___', inline=False)
                                embeds = _build_embed(embeds, section[section_info])
                    return embeds
                return []

        def _build_embed(embeds, section):
            def _build_lectures(lectures):
                for lecture in lectures:
                    yield ' '.join(_build_lecture(lecture))

            def _build_lecture(lecture):
                def _format_day(day):
                    return dict(csv.reader(open('bot/cogs/yorku_days.csv', 'r'))).get(day, '')

                def _format_times(time, duration):
                    def _format_time(time):
                        return datetime.strptime(str(time), "%H:%M:%S").strftime('%-I:%M %p')

                    hours, minutes = map(int, time.split(':'))
                    start = timedelta(hours=hours, minutes=minutes)
                    end = start + timedelta(minutes=int(duration))

                    return f'{_format_time(start)} to {_format_time(end)}'

                def _format_location(location):
                    return f'@{location}' if location != '\xa0 ' else ''

                def _format_backup(backup):
                    return f'- {backup}' if backup is not None else ''

                yield _format_day(lecture['Day'])
                yield _format_times(lecture['Start Time'], lecture['Duration'])
                yield _format_location(lecture['Location'])
                yield _format_backup(lecture.get('Backup'))

            for lecture in section:
                if len(section[lecture]['lectures']) > 0:
                    embeds.add_field(
                        name=f"{lecture}: {section[lecture].get('instructors', 'Not Available')}",
                        value='\n'.join(_build_lectures(section[lecture]['lectures'])),
                        inline=False
                    )
            return embeds

        error = "The requested course was not found. \n\
            \nCourses should be of the form: \
            \n\u2003\u2002[faculty] dept course [session year] \n\
            \nExamples: \
            \n\u2003\u2022 EECS 3311 \
            \n\u2003\u2022 LE EECS 3311 \
            \n\u2003\u2022 EECS 3311 FW 2020 \
            \n\u2003\u2022 LE EECS 3311 FW 2020"  

        course = ' '.join(context.message.content.split()[1:])
        info = re.match("".join((
            "(?:(?P<faculty>[a-z]{2})\s)?(?:(?P<department>[a-z]{2,4})\s?"
            "(?P<course>[0-9]{4}))+"
            "(?:\s(?P<session>[a-z]{2})\s?(?P<year>[0-9]{4}))?"
        )), course.lower())
        listings = list(scrape_course(info.groupdict()))
        if not len(listings):
            embed = discord.Embed(title="Error", description=error, color=0xff0000, inline=False)
            await context.channel.send(embed=embed)
        else:
            for listing in listings:
                for embed in _format_output(listing):
                    await context.channel.send(embed=embed)

def setup(client):
    client.add_cog(Course(client))
