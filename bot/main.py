import discord
from discord.ext import commands

import config
from commands import verify_user

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print('Ready!')

@client.event
async def on_message(message):
    await verify_user(message, client)

if __name__ == "__main__":
    client.run(config.TOKEN)
