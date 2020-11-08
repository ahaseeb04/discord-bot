import discord
from discord.ext import commands

from scrapers import scrape_course_list
from bot.embed_builder import EmbedBuilder

class CourseList(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def courselist(self, context):
        courses = ' '.join(context.message.content.split()[1:])
        course_list = scrape_course_list({'department': courses})

        embeds = EmbedBuilder(max_fields=24)
        for course in course_list:
            embeds.add_field(name=course[0], value=course[1])
        for embed in embeds: 
            await context.channel.send(embed=embed)


def setup(client):
    # client.add_cog(CourseList(client))
    pass
