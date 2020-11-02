import asyncio
import csv

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
    def check_reaction(message):
        def check(reaction, user):
            return reaction.message.id == message.id \
                and reaction.emoji == '👍' \
                and user.guild_permissions.manage_roles \
                and str(user.id) != config.bot_id

        return check

    if context.message.channel.name == config.verification_channel:
        try:
            await context.message.add_reaction(emoji='👍')
            await client.wait_for('reaction_add', check=check_reaction(context.message))
        except asyncio.TimeoutError as e:
            pass
        else:
            roles = { role.name.lower() : role.name for role in client.get_guild(int(config.server_id)).roles }
            roles = { **roles, **aliases }

            requested_roles = [ role.strip() for role in context.message.content.split(';') ]

            for requested_role in requested_roles:
                requested = max(((ratio, role) for role in roles if (ratio := fuzz.token_sort_ratio(role, requested_role)) > 70), default=None)

                if requested is None:
                    requested = max(((ratio, role) for role in roles if (ratio := fuzz.partial_ratio(role, requested_role.lower())) > 70), default=None)

                if requested is not None and len(role := roles.get(requested[1])):
                    await context.message.author.add_roles(get(context.message.author.guild.roles, name=role))

                    print(f'{role} role assigned.')

if __name__ == "__main__":
    aliases = { key : value.strip() for key, value in csv.reader(open('bot/aliases.csv', 'r')) }

    client.run(config.token)
