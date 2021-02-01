from discord.ext import commands

from ._cog import _Cog
from bot import config

class Brady(_Cog):
    @commands.has_permissions(manage_roles=True)
    @commands.command(brief="Post as Brady.")
    async def brady(self, context, **kwargs):
        await context.message.delete()
        msg = context.message.content.replace(f'{context.prefix}{context.command}', '', 1)
        for word in context.message.content.split():
            try:
                repl = await context.fetch_message(int(word.replace('?', '')))
                msg = msg.replace(word, '', 1)
                await repl.reply(msg)
                return
            except Exception:
                pass
        for channel in self.client.get_guild(int(config.server_id)).channels:
            if f'{context.prefix}{channel}' in msg:
                msg = msg.replace(f'{context.prefix}{channel}', '', 1)
                await channel.send(msg)
                return

        await context.channel.send(msg)