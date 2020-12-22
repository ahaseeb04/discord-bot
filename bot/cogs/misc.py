import math
from pytz import timezone
from random import randrange, randint

import aiocron
import discord
from discord.utils import get

from ._cog import _Cog
from bot import config

class CronJobs(_Cog):
    def __init__(self, client):
        _Cog.__init__(self, client)
        tz = timezone('US/Eastern')

        @aiocron.crontab('0 10 * * *', tz=tz)
        async def js():
            await self.daily_reminder(config.cs_channel, "Daily reminder JS is ass")

        @aiocron.crontab('0 19 * * *', tz=tz)
        async def js():
            await self.daily_reminder(config.cs_channel, "Daily reminder Angular is ass")

        @aiocron.crontab('0 10 * * *', tz=tz)
        async def hey():
            await self.daily_reminder(config.engineering_channel, "Hey")

        @aiocron.crontab('0 19 * * *', tz=tz)
        async def destiny():
            await self.daily_reminder(config.gaming_channel, "Daily reminder Destiny is ass")

    async def daily_reminder(self, channel, message):
        await self.client.get_channel(int(channel)).send(message)


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

class DestinySucks(_Cog):
    @_Cog.listener(name='on_message')
    async def destiny_sucks(self, message):
        if 'destiny' in message.content.lower() and randint(1, 4) == 2 and message.author.id != int(config.bot_id):
            await message.channel.send('Destiny is ass')
