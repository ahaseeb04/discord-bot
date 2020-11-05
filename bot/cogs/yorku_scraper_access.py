import re
import csv
from datetime import datetime, timedelta

import discord
from discord.ext import commands

import scraper
import config


class YorkuScraper(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def course(self, context):
        def format_output(info):
            if info.get('error') is not None:
                return discord.Embed(title="Error", description=info['error'], color=0xff0000, inline=False)
            else:
                embed = discord.Embed(title=info['heading'], description=info['description'], color=0x0000ff, inline=False, url=info['url'])
                for section in info['sections']:
                    for sect in section:
                        if section[sect] == "Cancelled":
                            embed.add_field(name='\u200b', value=f'___***{sect}***___\n{section[sect]}', inline=False)
                        else:
                            embed.add_field(name='\u200b', value=f'___***{sect}***___', inline=False)
                            embed = build_embed(embed, section[sect])
                return embed

        def build_embed(embed, section):
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

                print(lecture)
                yield format_day(lecture['Day'])
                yield format_times(lecture['Start Time'], lecture['Duration'])
                yield format_location(lecture['Location'])
                yield format_backup(lecture.get('Backup'))

            for lect in section:
                embed.add_field(
                    name=f"{lect}: {section[lect].get('instructors', 'Not Available')}",
                    value='\n'.join(build_lectures(section[lect]['lectures'])),
                    inline=False
                )
            return embed

        course = ' '.join(context.message.content.split()[1:])
        info = re.match("(?:(?P<faculty>[a-z]{2})\s)?(?:(?P<department>[a-z]{2,4})\s?(?P<course>[0-9]{4}))+(?:\s(?P<session>[a-z]{2})\s?(?P<year>[0-9]{4}))?", course.lower())
        embed = format_output(scraper.scrape_course(info.groupdict()))

        await context.channel.send(embed=embed)


def setup(client):
    client.add_cog(YorkuScraper(client))