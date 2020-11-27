import asyncio
from datetime import date, datetime

from fuzzywuzzy import fuzz
from discord.utils import get
from discord.ext import commands

from ._cog import _Cog
from bot import config
from bot.utils import get_user
from database_tools import df_to_dict, sql_to_df, dict_to_df, df_to_sql, engine
from bot.exceptions import IllegalFormatError, NotApprovedError, WrongChannelError

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

                if requested is not None and (role := roles.get(requested[1])) is not None:
                    yield get(context.message.author.guild.roles, name=role)

        try:
            if context.message.channel.id != int(config.verification_channel):
                raise WrongChannelError()

            await context.message.channel.send(f'{context.message.author.mention} A moderator is currently reviewing your verification request and will get back to you shortly.')

            logs_channel = self.client.get_channel(int(config.verification_logs_channel))
            await logs_channel.send(context.message.content)

            user_embed = await logs_channel.send(embed=get_user(context, context.message.author))

            reactions = ['👍', '👎', '❌']
            for reaction in reactions:
                await user_embed.add_reaction(emoji=reaction)

            await self.client.wait_for('reaction_add', timeout=60*60*24, check=check_reaction(user_embed))
        except IllegalFormatError:
            channel = self.client.get_channel(int(config.verification_rules_channel))
            await context.message.channel.send(f'{context.message.author.mention} Sorry, please check {channel.mention} and try again!')
        except NotApprovedError:
            await context.message.author.kick()
            await context.message.channel.send(f'{context.message.author} has been kicked from server.')
        except WrongChannelError:
            channel = self.client.get_channel(int(config.verification_channel))
            await context.message.channel.send(f'The verification command can only be used in {channel.mention}.')
        except asyncio.TimeoutError as e:
            print(e)
        else:
            user = context.message.author

            eng = engine(url=config.postgres_url, params=config.postgres_params)
            roles = { role.name.lower() : role.name for role in self.client.get_guild(int(config.server_id)).roles }
            aliases = df_to_dict(sql_to_df('aliases', eng, 'alias')['role'])

            roles = { **roles, **aliases }

            await user.add_roles(*get_requested_roles())
            await context.message.channel.send(f'{user.mention} has been verified.')

            df = sql_to_df('last_message', eng, 'user_id')
            df.at[str(user.id), 'verified'] = date.today().isoformat()
            df_to_sql(df, 'last_message', eng)
        finally:
            await user_embed.clear_reactions()
