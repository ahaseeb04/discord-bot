import discord
from discord.ext import commands
from discord.utils import get

import config
from utils import to_upper, to_lower, to_cap, to_title

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print('Ready!')

@client.command()
async def verify(context):
    if context.message.author == client.user:
        return

    async def assign_role(requested, func, case):
        if func(requested) in case:
            await context.message.author.add_roles(get(context.message.author.guild.roles, name=func(requested)))

            print('Role assigned.')

    if context.message.channel.name == config.verification_channel:
        roles = { role.name for role in client.get_guild(int(config.server_id)).roles }
        requestedRoles = context.message.content.split()

        upper = { role for role in roles if role.isupper() }
        lower = { role for role in roles if role.islower() }
        cap = { role for role in roles if role[0].isupper() and role[1:].islower() }
        title = { role for role in roles if role.title() }

        for requested in requestedRoles:
            await assign_role(requested, to_upper, upper)
            await assign_role(requested, to_lower, lower)
            await assign_role(requested, to_cap, cap)
            await assign_role(requested, to_title, title)

if __name__ == "__main__":
    client.run(config.token)
