#!/usr/bin/env python3
import os
import subprocess
import discord
from dotenv import load_dotenv

load_dotenv()

client = discord.Client()


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


def getCommand(message):
    content = str(message.content).split(" ")
    command = os.environ.get("PHP_PATH") + " " + os.environ.get("KORRIBAN_SENTINEL_PATH") + " " + os.environ.get("COMMAND_PREFIX")
    if content[1] == "register":
        return command + content[1] + " " + str(message.author.id) + " " + str(message.author.name) + " " + content[2]
    elif content[1] == "ally" or content[1] == "snapshot":
        return command + content[1] + " " + str(message.author.id) + " " + str(message.author.name)
    else:
        raise Exception("missing command: " + str(content))


def mentionAdmin():
    return "<@" + os.environ.get("ADMIN_ID") + ">"


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("-ks"):
        await message.add_reaction("⌛")
        try:
            command = getCommand(message)
            result = subprocess.check_output(command, shell=True).decode("utf-8")
            await message.clear_reactions()
            await message.add_reaction("✅")
        except Exception as error:
            result = "Something went wrong, call " + mentionAdmin() + "!\n" + repr(error)
            await message.clear_reactions()
            await message.add_reaction("❌")

        await message.channel.send(result)


client.run(os.environ.get("DISCORD_BOT_TOKEN"))
