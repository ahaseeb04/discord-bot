import math
from pytz import timezone
from random import randrange

import aiocron
import discord
from discord.utils import get
from discord.ext import commands

from ._cog import _Cog
from bot import config

class Main(_Cog):
    @_Cog.listener()
    async def on_ready(self):
        print("Ready!")

    @_Cog.listener()
    async def on_command_error(self, context, error):
        if isinstance(error, commands.CommandNotFound):
            await context.message.channel.send(error)
        else:
            print(error)

    @_Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.message.channel.id == int(config.verification_channel) and reaction.message.content.startswith(';verify'):
            if not reaction.message.author.guild_permissions.manage_roles and str(user.id) != config.bot_id:
                await reaction.message.remove_reaction(emoji=reaction.emoji, member=user)

class CronJobs(_Cog, name='js'):
    def __init__(self, client):
        _Cog.__init__(self, client)
        tz = timezone('US/Eastern')
        aiocron.crontab('0 10 * * *', func=self.daily_reminder, tz=tz)
        aiocron.crontab('0 10 * * *', func=self.daily_hey, tz=tz)

    async def daily_reminder(self):
        await self.client.get_channel(int(config.cs_channel)).send("Daily reminder js is ass")

    async def daily_hey(self):
        await self.client.get_channel(int(config.engineering_channel)).send("Hey")

class StfuuuuuAunk(_Cog):
    @_Cog.listener(name='on_message')
    async def stfuuuuu_aunk(self, message):
        def fire(msg):
            chance = math.ceil(500**2 / (len(msg)**2 or 1))
            return not (chance and randrange(chance))

        guild = self.client.get_guild(int(config.server_id))
        author = guild.get_member(message.author.id)
        if author is not None and any(str(role.id) == config.stfuuuuu_aunk for role in author.roles) and fire(message.content):
            role = get(message.guild.roles, id=int(config.stfuuuuu_aunk))
            await message.channel.send(role.mention)
