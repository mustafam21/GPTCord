import discord
from discord import app_commands



class DiscordClient(discord.Client):
    def __init__(self, *, intents=discord.Intents.default()) -> None:
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.activity = discord.Activity(
            type=discord.ActivityType.watching, name="/chat"
        )