import json
import os
import platform
import random
import sys
import typing

import aiohttp
import disnake
from disnake.ext import commands
from disnake.ext.commands import Context

from helpers.sql_manager import CountingChannel, CountingMember

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

class Channel(commands.Cog, name="channel"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="addchannel",
        description="Designate a channel for counting",
    )
    async def add_channel(self, context: Context,
        channel: disnake.TextChannel, count_type: str,
        last_count: typing.Optional[str] = "", score: typing.Optional[int] = 0) -> None:

        CountingChannel.create(channel.id, last_count, 0, count_type, score)
        await context.reply("Counting channel set!")

def setup(bot):
    bot.add_cog(Channel(bot))
