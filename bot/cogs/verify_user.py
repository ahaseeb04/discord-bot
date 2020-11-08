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
                can_perform_action = reaction.message.id == message.id and user.guild_permissions.manage_roles and str(user.id) != config.bot_id

                if reaction.emoji == '👍' and can_perform_action:
                    return True
                elif reaction.emoji == '👎' and can_perform_action:
                    raise IllegalFormatException()

            return check

        def get_requested_roles():
            requested_roles = [ role.strip() for role in context.message.content.split(self.client.command_prefix) ]

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
                await context.message.add_reaction(emoji='👎')

                try:
                    await self.client.wait_for('reaction_add', timeout=86400, check=check_reaction(context.message))
                except IllegalFormatException:
                    await context.message.channel.send(f'<@{context.message.author.id}> Sorry, please read <#{config.verification_rules_channel}> and try again.')
                    return
            except asyncio.TimeoutError as e:
                pass
            else:
                for requested in requested_roles:
                    if requested is not None and len(role := roles.get(requested[1])):
                        await context.message.author.add_roles(get(context.message.author.guild.roles, name=role))

                        print(f'{role} role assigned.')

class IllegalFormatException(Exception):
    pass

def setup(client):
    client.add_cog(VerifyUser(client))
