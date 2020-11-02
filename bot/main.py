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
    if context.message.author == client.user:
        return

    def react_check(message):
        def check(reaction, user):
            return reaction.message.id == message.id \
                and reaction.emoji == '👍' \
                and user.guild_permissions.manage_roles \
                and str(user.id) != config.bot_id
        return check

    def get_requested_roles():
        requested_roles = [ role.strip() for role in context.message.content.split(';') ]

        for requested_role in requested_roles:
            requested = max(((ratio, role) for role in roles if (ratio := fuzz.token_sort_ratio(role, requested_role)) > 70), default=None)
            if requested is None:
                requested = max(((ratio, role) for role in roles if (ratio := fuzz.partial_ratio(role, requested_role.lower())) > 70), default=None)
            yield requested

    if context.message.channel.name == config.verification_channel:
        try:
            roles = { role.name.lower() : role.name for role in client.get_guild(int(config.server_id)).roles }
            roles = { **roles, **aliases }

            requested_roles = list(get_requested_roles())

            await context.message.add_reaction(emoji='👍')
            await client.wait_for('reaction_add', check=react_check(context.message))
        except asyncio.TimeoutError as e:
            print(e)
        else:
            for requested in requested_roles:
                if requested is not None and len(role := roles.get(requested[1])):
                    await context.message.author.add_roles(get(context.message.author.guild.roles, name=role))

                    print(f'{role} role assigned.')

if __name__ == "__main__":
    aliases = { key :  val.strip() for key, val in csv.reader(open('bot/aliases.csv', 'r')) }

    client.run(config.token)