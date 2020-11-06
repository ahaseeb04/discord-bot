import re
import csv
from datetime import datetime, timedelta

import discord
from discord.ext import commands

import scraper
import config


class EmbedBuilder():
    def __init__(self, **kwargs):
        self.properties = {
            'color' : kwargs.get('color', ''),
            'title' : kwargs.get('title', ''),
            'url' : kwargs.get('url', ''),
            'thumbnail' : kwargs.get('thumbnail', discord.Embed.Empty)
        }
        self.thumbnail = kwargs.pop('thumbnail', discord.Embed.Empty)
        self.embeds = [discord.Embed(**kwargs).set_thumbnail(url=self.properties['thumbnail'])]

    def add_field(self, **kwargs):
        embed = self.embeds[-1]
        if len(embed.fields) == 25:
            embed = discord.Embed(**self.properties).set_thumbnail(url=self.properties['thumbnail'])
            self.embeds.append(embed)
        embed.add_field(**kwargs)

    def __iter__(self):
        return iter(self.embeds)

class GetCourse(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def course(self, context):
        def format_output(info):
            error = "The requested course was not found. \n\
                \nCourses should be of the form: \
                \n\u2003\u2002[faculty] dept course [session year] \n\
                \nExamples: \
                \n\u2003\u2022 EECS 3311 \
                \n\u2003\u2022 LE EECS 3311 \
                \n\u2003\u2022 EECS 3311 FW 2020 \
                \n\u2003\u2022 LE EECS 3311 FW 2020"  

            if info.get('error', None) is not None:
                return EmbedBuilder(title="Error", description=error, color=0xff0000, inline=False)
            else:
                embeds = EmbedBuilder(
                    title=info['heading'], 
                    description=info['description'],
                    color=0x0000ff, 
                    url=info['url'],
                    thumbnail='http://continue.yorku.ca/york-scs/wp-content/uploads/2016/06/YorkU-logo6.jpg'
                )
                header = '\u200b'
                for section in info['sections']:
                    for sect in section:
                        if section[sect] == "Cancelled":
                            embeds.add_field(name=header, value=f'___***{sect}***___\n{section[sect]}', inline=False)
                        else:
                            embeds.add_field(name=header, value=f'___***{sect}***___', inline=False)
                            embeds = build_embed(embeds, section[sect])
                return embeds

        def build_embed(embeds, section):
            def build_lectures(lectures):
                for lecture in lectures:
                    yield ' '.join(build_lecture(lecture))

            def build_lecture(lecture):
                def format_day(day):
                    return dict(csv.reader(open('bot/cogs/yorku_days.csv', 'r'))).get(day, '')

                def format_times(time, duration):
                    def format_time(time):
                        return datetime.strptime(str(time), "%H:%M:%S").strftime('%-I:%M %p')

                    hours, minutes = map(int, time.split(':'))
                    start = timedelta(hours=hours, minutes=minutes)
                    end = start + timedelta(minutes=int(duration))

                    return f'{format_time(start)} to {format_time(end)}'

                def format_location(location):
                    return f'@{location}' if location != '\xa0 ' else ''

                def format_backup(backup):
                    return f'- {backup}' if backup is not None else ''

                yield format_day(lecture['Day'])
                yield format_times(lecture['Start Time'], lecture['Duration'])
                yield format_location(lecture['Location'])
                yield format_backup(lecture.get('Backup'))

            for lect in section:
                embeds.add_field(
                    name=f"{lect}: {section[lect].get('instructors', 'Not Available')}",
                    value='\n'.join(build_lectures(section[lect]['lectures'])),
                    inline=False
                )
            return embeds

        course = ' '.join(context.message.content.split()[1:])
        info = re.match("(?:(?P<faculty>[a-z]{2})\s)?(?:(?P<department>[a-z]{2,4})\s?(?P<course>[0-9]{4}))+(?:\s(?P<session>[a-z]{2})\s?(?P<year>[0-9]{4}))?", course.lower())
        embeds = format_output(scraper.scrape_course(info.groupdict()))
        for embed in embeds:
            await context.channel.send(embed=embed)

def setup(client):
    client.add_cog(GetCourse(client))
