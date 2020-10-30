from discord.utils import get

import config

async def verify_user(message, client):
    if message.author == client.user:
        return

    if str(message.channel) == 'general' and message.content.startswith('!verify'):
        roles = [role.name.lower() for role in client.get_guild(int(config.SERVER_ID)).roles]
        requestedRoles = message.content.split()

        for requested in requestedRoles:
            if requested.lower() in roles:
                await message.author.add_roles(get(message.author.guild.roles, name=requested))

                print('Role assigned.')
