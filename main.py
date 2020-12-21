import inspect

from discord import Intents
from discord.ext import commands

from bot import config
from bot.cogs._cog import _Cog

if __name__ == "__main__":
    client = commands.Bot(command_prefix=';', intents=Intents.all())

    for cog in _Cog.__subclasses__():
        print(cog)
        client.add_cog(cog(client))

    client.run(config.token)
