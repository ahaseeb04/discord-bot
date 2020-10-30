from discord.utils import get

import config
from utils import to_upper, to_lower, to_cap, to_title

async def verify_user(message, client):
    async def verify(requested, func, case):
        if func(requested) in case:
            await message.author.add_roles(get(message.author.guild.roles, name=func(requested)))
            print('Role assigned.')


    if message.author == client.user:
        return

    if message.channel.name == 'general' and message.content.startswith('!verify'):
        roles = [ role.name for role in client.get_guild(int(config.SERVER_ID)).roles ]
        requestedRoles = message.content.split()
        
        up = { role for role in roles if role.isupper()}
        cap = { role for role in roles if role[0].isupper() and role[1:].islower()}
        low = { role for role in roles if role.islower()}
        title = { role for role in roles if role.title()}

        print(up, low, cap, title)

        for requested in requestedRoles:
            await verify(requested, to_upper, up)
            await verify(requested, to_lower, low)
            await verify(requested, to_cap, cap)
            await verify(requested, to_title, title)