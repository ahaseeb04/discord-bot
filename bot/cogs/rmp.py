import discord
from discord.ext import commands

import scraper

class Rmp(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def rmp(self, context):
        professor_name = context.message.content.lower().split()[1:]

        try:
            data = scraper.scrape_rmp(professor_name)

            embed = discord.Embed(title=data['name'], url=data['hyperlink'], color=0x00ff00)

            embed.set_thumbnail(url='https://i.imgur.com/0eDVqDp.png')

            embed.add_field(name='Top review', value=data['review'], inline=False)
            embed.add_field(name='Rating', value=data['rating'] + '/5', inline=False)
            embed.add_field(name='Difficulty', value=data['difficulty'], inline=False)
            embed.add_field(name='Would take again', value=data['take_again'], inline=False)

            await context.message.channel.send(embed=embed)
        except Exception:
            await context.message.channel.send('**Error**: Sorry, could not find professor!')

def setup(client):
    client.add_cog(Rmp(client))
