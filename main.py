import inspect
import csv

import discord
from discord.ext import commands

from bot import config, cogs
from bot.cogs._cog import _Cog

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
client = commands.Bot(command_prefix=';', intents=intents)

@client.event
async def on_ready():
    print('Ready!')

@client.event
async def on_command_error(context, error):
    if isinstance(error, commands.CommandNotFound):
        await context.message.channel.send(error)
    else:
        print(error)

if __name__ == "__main__":
    for cog in _Cog.__subclasses__():
        print(cog)
        client.add_cog(cog(client))

    client.run(config.token)