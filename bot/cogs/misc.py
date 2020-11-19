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

        author = message.guild.get_member(message.author.id)
        if author is not None and any(str(role.id) == config.stfuuuuu_aunk for role in author.roles) and fire(message.content):
            role = get(message.guild.roles, id=int(config.stfuuuuu_aunk))
            await message.channel.send(role.mention)
