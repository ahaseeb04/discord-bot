from datetime import datetime
from pytz import timezone

import discord


from database_tools import engine, sql_to_df, redis_access
from bot import config
from database_tools import engine, sql_to_df

def get_user(context, user):
    eng = engine(url=config.postgres_url, params=config.postgres_params)
    df = sql_to_df('last_message', eng, 'user_id')
    redis = redis_access(url=config.redis_url, params=config.redis_params)

    roles = [ role.mention for role in user.roles if role.name != '@everyone' ]
    color = user.color if len(roles) > 0 and str(user.color) != '#000000' else 0xdb2777

    embed = discord.Embed(description=user.mention, color=color)

    embed.set_author(name=user, icon_url=user.avatar_url)
    embed.set_thumbnail(url=user.avatar_url)

    tz = timezone('US/Eastern')
    frmt_str = "%a %b %-d, %Y @ %-I:%M %p"

    embed.add_field(name='Registered', value=user.created_at.astimezone(tz).strftime(frmt_str), inline=False)
    embed.add_field(name='Joined at', value=user.joined_at.astimezone(tz).strftime(frmt_str), inline=False)
    if (last_message := redis.hmget('users', str(user.id))[0] or df.last_message.get(str(user.id))) is not None:
        last_message = datetime.strptime(last_message, "%Y-%m-%d").astimezone(tz)
        embed.add_field(name="Last message", value=last_message.strftime('%a %b %-d, %Y'), inline=False)

    if len(roles) > 0:
        embed.add_field(name=f'Roles [{len(roles)}]', value=' '.join(reversed(roles)), inline=False)

    return embed
