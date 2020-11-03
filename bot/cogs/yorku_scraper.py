import re

import discord
from discord.ext import commands

import scraper


class YorkuScraper(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def course(self, context):
        course = ' '.join(context.message.content.split()[1:])
        info = re.match("(?:(?P<faculty>[a-z]{2})\s)?(?:(?P<department>[a-z]{2,4})\s(?P<number>[0-9]{4}))+(?:\s(?P<session>[a-z]{2})\s(?P<year>[0-9]{4}))?", course.lower())
        info = scraper.scrape_course(info.groupdict())
        if info.get('error') is not None:
            emb = discord.Embed(title="Error", description=info['error'], color=0xff0000)
        else:
            emb = discord.Embed(title=info['heading'], description=info['description'], color=0x0000ff)
            for section in info['sections']:
                for sect in section:
                    if section[sect] == 'Cancelled':
                        val = 'Cancelled'
                    else:
                        val = []
                        for lect in section[sect]:
                            l = []
                            l.append(lect)
                            l.append(section[sect][lect].get('instructors', 'Not Available'))
                            val.append(': '.join(l))
                            for lecture in section[sect][lect]['lectures']:
                                val.append('\t'.join(lecture.values()))

                        val = '\n'.join(val)
                    emb.add_field(name=sect, value=val, inline=False)


        await context.channel.send(embed=emb)


def setup(client):
    client.add_cog(YorkuScraper(client))