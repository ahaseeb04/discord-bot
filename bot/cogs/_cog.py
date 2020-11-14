import abc
import sys
import inspect

from discord.ext import commands

class _MetaCog(commands.CogMeta, abc.ABCMeta):
    pass

class _Cog(commands.Cog, abc.ABC, metaclass=_MetaCog):
    def __init__(self, client):
        self.client = client
