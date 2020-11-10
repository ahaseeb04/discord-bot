from pytz import timezone

import discord
from discord.ext import tasks, commands
import aiocron

from ._cog import _Cog
from bot import config

class DailyReminder(_Cog, name='js'):
    def __init__(self, client):
        _Cog.__init__(self, client)
        aiocron.crontab('0 10 * * *', func=self.daily_reminder, start=True, tz=timezone('US/Eastern'))

    async def daily_reminder(self):
        await self.client.get_channel(int(config.cs_channel)).send("Daily reminder js is ass")