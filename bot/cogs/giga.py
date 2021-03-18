from discord.ext import commands

from ._cog import _Cog
from bot import config

class Giga(_Cog):
    @commands.command(brief="Post as the bot.", hidden=True)
    async def giga(self, context, **kwargs):
        allowed_users = [364856110806728707, 481633326831108096, 266218689718648832]

        if context.message.author.id in allowed_users:
            await context.message.delete()
            msg = context.message.content.replace(f'{context.prefix}{context.command}', '', 1)
            for word in context.message.content.split():
                try:
                    repl = await context.fetch_message(int(word.replace(f'{context.prefix}', '', 1)))
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
