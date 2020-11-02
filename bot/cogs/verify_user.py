import csv
import asyncio

from fuzzywuzzy import fuzz
from discord.utils import get
from discord.ext import commands

import config

class VerifyUser(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def verify(self, context):
        def check_reaction(message):
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
                roles = { role.name.lower() : role.name for role in self.client.get_guild(int(config.server_id)).roles }
                aliases = { key : value.strip() for key, value in csv.reader(open('bot/aliases.csv', 'r')) }

                roles = { **roles, **aliases }

                requested_roles = list(get_requested_roles())

                await context.message.add_reaction(emoji='👍')
                await self.client.wait_for('reaction_add', timeout=86400, check=check_reaction(context.message))
            except asyncio.TimeoutError as e:
                pass
            else:
                for requested in requested_roles:
                    if requested is not None and len(role := roles.get(requested[1])):
                        await context.message.author.add_roles(get(context.message.author.guild.roles, name=role))

                        print(f'{role} role assigned.')

def setup(client):
    client.add_cog(VerifyUser(client))
