import os
import inspect
import csv

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
        if issubclass(type(cog[1]), type(commands.Cog)):
            client.load_extension(cog[1].__module__)

    client.run(config.token)
