from abc import ABC
from discord import Message, Embed

class Dialog(ABC):
    def __init__(self, *args, **kwargs):
        self.embed: Embed = None
        self.message: Message = None
        self.color: hex = kwargs.get('color') or 0x000000

    async def quit(self, text: str = None):
        if text is None:
            await self.message.delete
        else:
            await self.message.edit(content=text, embed=None)
            await self.message.clear_reactions()

    async def update(self, text: str, color: hex = None, hide_author: bool = False):
        if color is None:
            color = self.color

        self.embed.color = color
        self.embed.title = text

        if hide_author:
            self.embed.set_author(name='')

        await self.display(embed=self.embed)

    async def display(self, text: str = None, embed: Embed = None):
        await self.message.edit(content=text, embed=embed)
