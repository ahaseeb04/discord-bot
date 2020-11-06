
import discord
from discord.ext import commands

import scraper

class EmbedBuilder():
    def __init__(self, **kwargs):
        self.properties = {
            'color' : kwargs.get('color', discord.Embed.Empty),
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

class CourseList(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def courselist(self, context):
        courses = ' '.join(context.message.content.split()[1:])
        course_list = scraper.scrape_course_list({'department': courses})

        embeds = EmbedBuilder()
        for course in course_list:
            embeds.add_field(name=course[0], value=course[1], inline=False)
        for embed in embeds: 
            await context.channel.send(embed=embed)


def setup(client):
    client.add_cog(CourseList(client))
