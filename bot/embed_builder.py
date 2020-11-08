import discord

class EmbedBuilder():
    def __init__(self, **kwargs):
        self.properties = {
            'color' : kwargs.get('color', discord.Embed.Empty),
            'title' : kwargs.get('title', ''),
            'url' : kwargs.get('url', ''),
        }
        self.max_fields = kwargs.get('max_fields', 25)
        self.thumbnail = kwargs.pop('thumbnail', discord.Embed.Empty)
        self.embeds = [discord.Embed(**kwargs).set_thumbnail(url=self.thumbnail)]

    def add_field(self, **kwargs):
        embed = self.embeds[-1]
        if len(embed.fields) == self.max_fields:
            embed = discord.Embed(**self.properties).set_thumbnail(url=self.thumbnail)
            self.embeds.append(embed)
        embed.add_field(**kwargs)

    def __iter__(self):
        return iter(self.embeds)