from pytz import timezone
from random import randrange

import discord
from discord.ext import tasks, commands
import aiocron

from ._cog import _Cog
from bot import config

class DailyReminder(_Cog):
    def __init__(self, client):
        _Cog.__init__(self, client)
        aiocron.crontab('0 10 * * *', func=self.daily_reminder, start=True, tz=timezone('US/Eastern'))

    async def daily_reminder(self):
        await self.client.get_channel(int(config.cs_channel)).send("Daily reminder js is ass")

class StfuuuuuAunk(_Cog):
    @_Cog.listener(name='on_message')
    async def stfuuuuu_aunk(self, message):
        if config.stfuuuuu_aunk in { str(role.id) for role in message.author.roles } and not randrange(25):
            await message.channel.send(message.content)