import datetime as dt
import asyncio
from pytz import timezone

from discord.ext import commands
from disputils import BotEmbedPaginator
import discord
import pandas as pd

from ._cog import _Cog
from bot import config
from bot.exceptions import DataNotFoundError
from database_tools import engine, sql_to_df, redis_access


class User(_Cog, name="user"):
    @commands.command(brief='Fetch details for a spcified user.', aliases=['member', 'u', 'whois'])
    async def user(self, context):
        try:
            guild = self.client.get_guild(int(config.server_id))
            users = [ guild.get_member(int(c)) for c in context.message.content.split() if c.isnumeric() ]
            embeds = [ await get_user(context, user) for user in set(context.message.mentions + users) if user is not None ]
            
            if not len(embeds):
                raise DataNotFoundError()
            
        except DataNotFoundError:
            await context.message.channel.send('**Error**: Sorry, please specify a valid user.')
        else:
            await BotEmbedPaginator(context, embeds).run()

    @commands.command(brief='Fetch details about yourself.')
    async def me(self, context):
        await context.message.channel.send(embed=await get_user(context, context.message.author))


async def get_user(context, user):
    await asyncio.sleep(0.01)
    eng = engine(url=config.postgres_url, params=config.postgres_params)
    df = sql_to_df('last_message', eng, 'user_id')
    redis = redis_access(url=config.redis_url, params=config.redis_params)

    roles = [ role.mention for role in user.roles if role.name != '@everyone' ]
    color = user.color if len(roles) > 0 and str(user.color) != '#000000' else 0xdb2777

    embed = discord.Embed(description=user.mention, color=color)

    embed.set_author(name=user, icon_url=user.avatar_url)
    embed.set_thumbnail(url=user.avatar_url)

    tz = timezone('US/Eastern')
    date_fmt = "%a, %b %-d, %Y @ %-I:%M %p"

    embed.add_field(name='Registered', value=user.created_at.astimezone(tz).strftime(date_fmt), inline=False)
    embed.add_field(name='Joined at', value=user.joined_at.astimezone(tz).strftime(date_fmt), inline=False)
    if (last_message := redis.hmget('users', str(user.id))[0] or df.last_message.get(str(user.id))) is not None:
        last_message = pd.to_datetime(last_message).tz_localize('UTC')
        fmt = date_fmt.split('@')[0] if last_message.time() == dt.time(0, 0) else date_fmt
        embed.add_field(name="Last message", value=last_message.astimezone(tz).strftime(fmt), inline=False)

    if len(roles) > 0:
        embed.add_field(name=f'Roles [{len(roles)}]', value=' '.join(reversed(roles)), inline=False)

    return embed

