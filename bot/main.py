import os
import inspect

import discord
from discord.ext import commands

import config
import cogs

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
client = commands.Bot(command_prefix=';', intents=intents)

@client.event
async def on_ready():
    print('Ready.')

if __name__ == "__main__":
    for cog in inspect.getmembers(cogs, inspect.isclass):
        client.load_extension(f'cogs.{cog[1].__module__}')

    client.run(config.token)
