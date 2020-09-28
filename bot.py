# bot.py
# Client handling updates to discord

import os
import json
import time

from discord.ext import commands
import discord
from dotenv import load_dotenv

from core.DataCollectionStrategy import is_valid_summoner_name

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

bot = commands.Bot(command_prefix="::")

@bot.command(name="hi", help="Checks if alive")
async def answer(ctx: commands.Context):
    response = "Who dis?"
    await ctx.send(response)

@bot.command(name="add", help="Adds to ints")
async def add(ctx: commands.Context, n1: int, n2: int):
    sum = n1 + n2
    response = f"{n1} + {n2} = {sum}"
    await ctx.send(response)

@bot.command(name="summoners", help="Shows who lp-bot is currently tracking")
async def summoners(ctx: commands.Context):
    summoners = json.loads(open("core/DataCollectionStrategy/summoners.json", "r", encoding="utf-8").read())
    response = f"Currently tracking: **{'**, **'.join(summoners[:-1])}** and **{summoners[-1]}**"
    await ctx.send(response)

@bot.command(name="add_summoner", help="Adds a new summoner to be tracked")
async def add_summoner(ctx: commands.Context, summoner_name: str):
    if is_valid_summoner_name(summoner_name):
        response = f"{summoner_name} has been added to the pool!\nAn update from the webhooks should occur in <=10 minutes."
    else:
        response = f"Could not find summoner {summoner_name}. Only tracking euw, might that be the problem?"
    await ctx.send(response)

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        delay = 10 # seconds
        content = message.content
        await message.edit(content=content+f"Will be deleted in **{delay} seconds**", delete_after=delay)


    if message.content == "::help":
        await message.delete()

bot.run(TOKEN)