import re

from discord.ext import commands

import scraper


class YorkuScraper(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def course(self, context):
        course = ' '.join(context.message.content.split()[1:])
        info = re.match("(?:(?P<faculty>[a-z]{2})\s)?(?:(?P<department>[a-z]{2,4})\s(?P<number>[0-9]{4}))+(?:\s(?P<session>[a-z]{2})\s(?P<year>[0-9]{4}))?", course.lower())
        res = scraper.scrape_course(info.groupdict())
        await context.channel.send(res)

def setup(client):
    client.add_cog(YorkuScraper(client))