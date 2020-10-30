import discord
from discord.ext import commands

import config


intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print('Ready!')

if __name__ == "__main__":
    client.run(config.TOKEN)
