import discord

async def get_user(context, user):
    roles = [ role.mention for role in user.roles if role.name != '@everyone' ]
    color = user.color if len(roles) > 0 or str(user.color) != '#000000' else 0xdb2777

    embed = discord.Embed(description=user.mention, color=color)

    embed.set_author(name=f'{user.name}#{user.discriminator}', icon_url=user.avatar_url)
    embed.set_thumbnail(url=user.avatar_url)

    embed.add_field(name='Registered', value=user.created_at.strftime("%c"), inline=True)
    embed.add_field(name='Joined at', value=user.joined_at.strftime("%c"), inline=True)

    if len(roles) > 0:
        embed.add_field(name=f'Roles [{len(roles)}]', value=', '.join(roles), inline=False)

    await context.message.channel.send(embed=embed)
