import csv
import asyncio

from fuzzywuzzy import fuzz
from discord.utils import get
from discord.ext import commands

from bot import config
from ._cog import _Cog
from bot.exceptions import IllegalFormatException, NotApprovedException

class VerifyUser(_Cog, name="verify"):
    @commands.command(brief='Request roles for yourself.')
    async def verify(self, context):
        def check_reaction(message):
            def check(reaction, user):
                can_manage_roles = reaction.message.id == message.id and user.guild_permissions.manage_roles and str(user.id) != config.bot_id
                can_kick_members = reaction.message.id == message.id and user.guild_permissions.kick_members and str(user.id) != config.bot_id

                if reaction.emoji == '👍' and can_manage_roles:
                    return True
                elif reaction.emoji == '👎' and can_manage_roles:
                    raise IllegalFormatException()
                elif reaction.emoji == '❌' and can_kick_members:
                    raise NotApprovedException()

            return check

        def get_requested_roles():
            requested_roles = [ role.strip() for role in context.message.content.split(self.client.command_prefix) ]

            for requested_role in requested_roles:
                requested = max(((ratio, role) for role in roles if (ratio := fuzz.token_sort_ratio(role, requested_role)) > 70), default=None)

                if requested is None:
                    requested = max(((ratio, role) for role in roles if (ratio := fuzz.partial_ratio(role, requested_role.lower())) > 70), default=None)

                yield requested

        if context.message.channel.id == int(config.verification_channel):
            try:
                roles = { role.name.lower() : role.name for role in self.client.get_guild(int(config.server_id)).roles }
                aliases = { key : value.strip() for key, value in csv.reader(open('bot/support/aliases.csv', 'r')) }

                roles = { **roles, **aliases }

                requested_roles = list(get_requested_roles())

                await context.message.add_reaction(emoji='👍')
                await context.message.add_reaction(emoji='👎')
                await context.message.add_reaction(emoji='❌')

                try:
                    await self.client.wait_for('reaction_add', timeout=86400, check=check_reaction(context.message))
                except IllegalFormatException:
                    channel = self.client.get_channel(int(config.verification_rules_channel))
                    await context.message.channel.send(f'{context.message.author.mention} Sorry, please check {channel.mention} and try again!')

                    return
                except NotApprovedException:
                    await context.message.author.kick()
                    await context.message.channel.send(f'{context.message.author} has been kicked from server.')

                    return
            except asyncio.TimeoutError as e:
                print(e)
            else:
                for requested in requested_roles:
                    if requested is not None and len(role := roles.get(requested[1])):
                        await context.message.author.add_roles(get(context.message.author.guild.roles, name=role))

                        print(f'{role} role assigned.')
