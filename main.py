import inspect

import discord
from discord.ext import commands

from bot import config
from bot.cogs._cog import _Cog

if __name__ == "__main__":
    intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
    client = commands.Bot(command_prefix=';', intents=intents)

    for cog in _Cog.__subclasses__():
        print(cog)
        client.add_cog(cog(client))

    client.run(config.token)