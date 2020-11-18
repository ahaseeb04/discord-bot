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
        self.embeds = []
        if kwargs.get('store', True):
            self.embeds.append(discord.Embed(**kwargs).set_thumbnail(url=self.thumbnail))
        self.description = kwargs.get('description')

    def add_field(self, **kwargs):
        embed = self.embeds[-1]
        if len(embed.fields) == self.max_fields:
            embed = discord.Embed(**self.properties).set_thumbnail(url=self.thumbnail)
            self.embeds.append(embed)
        embed.add_field(**kwargs)
        
    def insert_embed(self, embed):
        new_embed = discord.Embed(description=self.description, **self.properties).set_thumbnail(url=self.thumbnail)
        self.embeds.append(new_embed)
        self.merge_fields(embed)

    def merge_fields(self, embed):
        for field in embed.get_fields():
            self.add_field(name=field.name, value=field.value, inline=field.inline)

    def get_fields(self):
        return [field for embed in self.embeds for field in embed.fields]

    def __iter__(self):
        return iter(self.embeds)