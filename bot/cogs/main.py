import discord
from discord.ext import commands

from ._cog import _Cog
from bot import config
from .verify_user import VerifyUser

class Main(_Cog):
    @_Cog.listener()
    async def on_ready(self):
        print("Ready!")

    @_Cog.listener()
    async def on_command_error(self, context, error):
        pr = self.client.command_prefix
        if context.message.channel.id == int(config.verification_channel) and context.message.content.lower().startswith(f'{pr}verify{pr}'):
            await VerifyUser.verify(self, context)
        elif context.message.content == ';-;':
            pass
        elif isinstance(error, commands.CommandNotFound):
            await context.message.channel.send(error)
        elif isinstance(error, commands.MissingPermissions):
            err = context.message.content.split()[0].strip(pr)
            await context.message.channel.send(f'Command "{err}" is not found')
        else:
            print(error)

    @_Cog.listener()
    async def on_message(self, message):
        pr = self.client.command_prefix 
        if message.channel.id == int(config.verification_channel) and ''.join(message.content.lower().split()).startswith(f'verify{pr}'):
            context = await self.client.get_context(message)
            await VerifyUser.verify(self, context)