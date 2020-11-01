import asyncio
import discord
from fuzzywuzzy import fuzz
from discord.utils import get
from discord.ext import commands

import config

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
client = commands.Bot(command_prefix=';', intents=intents)

@client.event
async def on_ready():
    print('Ready!')

@client.command()
async def verify(context):
    if context.message.author == client.user:
        return

    def check(reaction, user):
        return str(reaction.emoji) == '👍' and user.guild_permissions.manage_roles and str(user.id) != config.automod_id

    if context.message.channel.name == config.verification_channel:
        try:
            await context.message.add_reaction(emoji='👍')
            await client.wait_for('reaction_add', check=check)
        except asyncio.TimeoutError as e:
            print(e)
        else:
            roles = { role.name.lower() : role.name for role in client.get_guild(int(config.server_id)).roles }
            requestedRoles = [ role.strip() for role in context.message.content.split(';') ]

            for requestedRole in requestedRoles:
                requested = max(((ratio, role) for role in roles if (ratio := fuzz.partial_ratio(role, requestedRole.lower())) > 70), default=None)

                if requested is not None:
                    await context.message.author.add_roles(get(context.message.author.guild.roles, name=roles[requested[1]]))
                    print(f'{requested[1]} role assigned.')




if __name__ == "__main__":
    client.run(config.token)
