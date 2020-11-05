import re
import csv
from datetime import datetime, timedelta

import discord
from discord.ext import commands

import scraper
import config


class EmbedBuilder():
    def __init__(self, title=None, description=None, color=None, url=None, thumbnail=None, inline=False):
        self.counter = 1
        self.color = color
        self.title = title
        self.url = url
        self.thumbnail = thumbnail
        self.embeds = []
        embed = discord.Embed(title=title, description=description, color=color, url=url, inline=inline)
        if self.thumbnail is not None:
            embed.set_thumbnail(url=self.thumbnail)
        self.embeds.append(embed)

    def add_field(self, name, value, inline=False):
        if self.counter % 25 == 0:
            embed = discord.Embed(title=self.title, url=self.url, color=self.color)
            embed.add_field(name=name, value=value, inline=inline)
            if self.thumbnail is not None:
                embed.set_thumbnail(url=self.thumbnail)
            self.embeds.append(embed)
            self.counter += 1
        else:
            self.embeds[-1].add_field(name=name, value=value, inline=inline)
            self.counter += 1

    def __iter__(self):
        return iter(self.embeds)




class YorkuScraper(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def course(self, context):
        def format_output(info):
            if info.get('error') is not None:
                return EmbedBuilder(title="Error", description=info['error'], color=0xff0000, inline=False)
            else:
                embeds = EmbedBuilder(
                    title=info['heading'], 
                    description=info['description'],
                     color=0x0000ff, 
                     url=info['url'],
                     thumbnail='http://continue.yorku.ca/york-scs/wp-content/uploads/2016/06/YorkU-logo6.jpg'
                )
                # embed = discord.Embed(title=info['heading'], description=info['description'], color=0x0000ff, inline=False, url=info['url'])
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
    client.add_cog(YorkuScraper(client))