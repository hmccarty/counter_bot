""""
Copyright © Krypton 2021 - https://github.com/kkrypt0nn (https://krypt0n.co.uk)
Description:
This is a template to create your own discord bot in python.

Version: 4.1
"""

import json
import os
import platform
import random
import sys
import sqlite3

import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import tasks, commands
from disnake.ext.commands import Bot
from disnake.ext.commands import Context

import exceptions
from helpers import counts
from helpers.sql_manager import CountingChannel, CountingMember

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

intents = disnake.Intents.default()

bot = Bot(command_prefix=config["prefix"], intents=intents)

@bot.event
async def on_ready() -> None:
    """
    The code in this even is executed when the bot is ready
    """
    print(f"Logged in as {bot.user.name}")
    print(f"disnake API version: {disnake.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")
    status_task.start()


@tasks.loop(minutes=1.0)
async def status_task() -> None:
    """
    Setup the game status task of the bot
    """
    await bot.change_presence(
        activity=disnake.Game("https://github.com/hmccarty/counter_bot")
    )


# Removes the default help command of discord.py to be able to create our custom help command.
bot.remove_command("help")

def load_commands(command_type: str) -> None:
    for file in os.listdir(f"./cogs/{command_type}"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                bot.load_extension(f"cogs.{command_type}.{extension}")
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")

if __name__ == "__main__":
    load_commands("counting")


@bot.event
async def on_message(message: disnake.Message) -> None:
    """
    The code in this event is executed every time someone sends a message, with or without the prefix
    :param message: The message that was sent.
    """
    if message.author == bot.user or message.author.bot:
        return

    # Check if sent in sent in a counting channel
    cc = CountingChannel.get(message.channel.id)
    if cc is not None:
        if counts.validate_count(cc.count_type, cc.last_count, message.content):
            # Prevent double counting
            if cc.last_counter == message.author.id:
                responses = ["How are you going to return your own serve?",
                             "Chill out and let someone else count",
                             "Counting is a team game",
                             "Take a break man, you're counting too hard"]
                await message.reply(random.choice(responses))
                return

            # Update score and last count
            cc.update(message.content, message.author.id)
            cm = CountingMember.get_or_create(message.author.id)
            cm.update(cm.score + 1)
        else:
            msg = await message.reply(
                f"That is not a valid count, current count is: {cc.last_count}. React to shame.")
            await msg.add_reaction("😡") # Rage emoji
    else:
        await bot.process_commands(message)

@bot.event
async def on_command_completion(context: Context) -> None:
    """
    The code in this event is executed every time a normal command has been *successfully* executed
    :param context: The context of the command that has been executed.
    """
    full_command_name = context.command.qualified_name
    split = full_command_name.split(" ")
    executed_command = str(split[0])
    print(
        f"Executed {executed_command} command in {context.guild.name} (ID: {context.message.guild.id}) by {context.message.author} (ID: {context.message.author.id})")


@bot.event
async def on_command_error(context: Context, error) -> None:
    """
    The code in this event is executed every time a normal valid command catches an error
    :param context: The normal command that failed executing.
    :param error: The error that has been faced.
    """
    if isinstance(error, commands.CommandOnCooldown):
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        embed = disnake.Embed(
            title="Hey, please slow down!",
            description=f"You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = disnake.Embed(
            title="Error!",
            description="You are missing the permission(s) `" + ", ".join(
                error.missing_permissions) + "` to execute this command!",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = disnake.Embed(
            title="Error!",
            description=str(error).capitalize(),
            # We need to capitalize because the command arguments have no capital letter in the code.
            color=0xE02B2B
        )
        await context.send(embed=embed)
    raise error


# Run the bot with the token
bot.run(config["token"])
