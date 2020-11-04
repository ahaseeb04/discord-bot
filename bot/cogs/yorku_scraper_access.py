import re

import discord
from discord.ext import commands

import scraper
import config


class YorkuScraper(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def course(self, context):
        def build_val(section):
            for lect in section:
                yield f"{lect}: {section[lect].get('instructors', 'Not Available')}"
                for lecture in section[lect]['lectures']:
                    yield '\t'.join(lecture.values())

        if context.message.channel.name != config.verification_channel:
            return
        course = ' '.join(context.message.content.split()[1:])
        info = re.match("(?:(?P<faculty>[a-z]{2})\s)?(?:(?P<department>[a-z]{2,4})\s?(?P<number>[0-9]{4}))+(?:\s(?P<session>[a-z]{2})\s?(?P<year>[0-9]{4}))?", course.lower())
        info = scraper.scrape_course(info.groupdict())
        if info.get('error') is not None:
            embed = discord.Embed(title="Error", description=info['error'], color=0xff0000, inline=False)
        else:
            embed = discord.Embed(title=info['heading'], description=info['description'], color=0x0000ff, inline=False)
            for section in info['sections']:
                for sect in section:
                    val = section[sect] if section[sect] == "Cancelled" else '\n'.join(build_val(section[sect])) 
                    embed.add_field(name=sect, value=val, inline=False)


        await context.channel.send(embed=embed,)


def setup(client):
    client.add_cog(YorkuScraper(client))