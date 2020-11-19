import asyncio
from datetime import date, datetime

from fuzzywuzzy import fuzz
from discord.utils import get
from discord.ext import commands

from bot import config
from bot.exceptions import IllegalFormatError, NotApprovedError, WrongChannelError
from ._cog import _Cog
from database_tools import df_to_dict, sql_to_df, dict_to_df, df_to_sql, engine

class VerifyUser(_Cog, name="verify"):
    @commands.command(brief='Request roles for yourself.')
    async def verify(self, context):
        def check_reaction(message):
            def check(reaction, user):
                has_permissions = lambda perms: getattr(user.guild_permissions, perms) and str(user.id) != config.bot_id
                is_correct_reaction = lambda emoji: reaction.message.id == message.id and reaction.emoji == emoji

                if is_correct_reaction('👍') and has_permissions('manage_roles'):
                    return True
                if is_correct_reaction('👎') and has_permissions('manage_roles'):
                    raise IllegalFormatError()
                if is_correct_reaction('❌') and has_permissions('kick_members'):
                    raise NotApprovedError()

            return check

        def get_requested_roles():
            requested_roles = [ role.strip() for role in context.message.content.split(self.client.command_prefix) ]

            for requested_role in requested_roles:
                requested = max(((ratio, role) for role in roles if (ratio := fuzz.token_sort_ratio(role, requested_role)) > 70), default=None)

                if requested is None:
                    requested = max(((ratio, role) for role in roles if (ratio := fuzz.partial_ratio(role, requested_role.lower())) > 70), default=None)

                yield requested

        try:
            if context.message.channel.id != int(config.verification_channel):
                raise WrongChannelError()

            eng = engine(db_url=config.postgres_url, db_params=config.postgres_params)
            roles = { role.name.lower() : role.name for role in self.client.get_guild(int(config.server_id)).roles }
            aliases = df_to_dict(sql_to_df('aliases', eng, 'alias')['role'])

            roles = { **roles, **aliases }

            requested_roles = list(get_requested_roles())

            await context.message.add_reaction(emoji='👍')
            await context.message.add_reaction(emoji='👎')
            await context.message.add_reaction(emoji='❌')

            await self.client.wait_for('reaction_add', timeout=86400, check=check_reaction(context.message))
        except IllegalFormatError:
            channel = self.client.get_channel(int(config.verification_rules_channel))
            await context.message.channel.send(f'{context.message.author.mention} Sorry, please check {channel.mention} and try again!')
        except NotApprovedError:
            await context.message.author.kick()
            await context.message.channel.send(f'{context.message.author} has been kicked from server.')
        except WrongChannelError:
            channel = self.client.get_channel(int(config.verification_channel))
            await context.message.channel.send(f'Command "verify" can only be used in {channel.mention}')
        except asyncio.TimeoutError as e:
            print(e)
        else:
            user = context.message.author
            for requested in requested_roles:
                if requested is not None and len(role := roles.get(requested[1])):
                    await user.add_roles(get(user.guild.roles, name=role))

                    print(f'{role} role assigned.')
            df = sql_to_df('last message', eng, 'user id')
            df.at[str(user.id), 'verified'] = date.today().isoformat()
            df_to_sql(df, 'last message', eng)
