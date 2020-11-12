from pytz import timezone
from random import randrange

import discord
from discord.ext import tasks, commands
from discord.utils import get
import aiocron

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

class DailyReminder(_Cog, name='js'):
    def __init__(self, client):
        _Cog.__init__(self, client)
        aiocron.crontab('0 10 * * *', func=self.daily_reminder, start=True, tz=timezone('US/Eastern'))

    async def daily_reminder(self):
        await self.client.get_channel(int(config.cs_channel)).send("Daily reminder js is ass")

class StfuuuuuAunk(_Cog):
    @_Cog.listener(name='on_message')
    async def stfuuuuu_aunk(self, message):
        chance = 1500 // len(message.content)
        if config.stfuuuuu_aunk in { str(role.id) for role in message.author.roles } and not randrange(chance):
            role = get(message.guild.roles, id=int(config.stfuuuuu_aunk))
            await message.channel.send(role.mention)