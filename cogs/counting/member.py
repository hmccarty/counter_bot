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

from helpers.sql_manager import CountingMember

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

class Member(commands.Cog, name="Member"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="score",
        description="Get score of counter",
    )
    async def score(self, context: Context) -> None:
        cm = CountingMember.get_or_create(context.author.id)
        await context.reply(f"Your score is: {cm.score}")

    @commands.command(
        name="leaderboard",
        description="Get top 10 counters",
    )
    async def leaderboard(self, context: Context) -> None:
        cms = CountingMember.get_best(context.author.id)

        desc = ""
        for i in range(len(cms)):
            desc += f"1. <@{cms[i].member_id}>: {cms[i].score}\n"

        msg = disnake.Embed(title="Counter Leaderboard", description=desc)
        await context.channel.send(embed=msg)

def setup(bot):
    bot.add_cog(Member(bot))
