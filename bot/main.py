import discord
from discord.ext import commands
from discord.utils import get
from fuzzywuzzy import fuzz


import config
# from utils import to_upper, to_lower, to_cap, to_title

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print('Ready!')

@client.command()
async def verify(context):
    if context.message.author == client.user:
        return

    if context.message.channel.name == config.verification_channel:
        roles = { role.name.lower() : role.name for role in client.get_guild(int(config.server_id)).roles }
        requestedRoles = context.message.content.split()


        for requested in requestedRoles:
            req = max(((ratio, role) for role in roles if (ratio := fuzz.partial_ratio(role, requested.lower())) > 75), default=None)
            if req is not None:
                await context.message.author.add_roles(get(context.message.author.guild.roles, name=roles[req[1]]))

                print('Role assigned.')

if __name__ == "__main__":
    client.run(config.token)
