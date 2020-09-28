# bot.py
# Client handling updates to discord

import os
import json
import time

from discord.ext import commands
from dotenv import load_dotenv

from core.DataCollectionStrategy import is_valid_summoner_name, add_summoner_to_pool

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

bot = commands.Bot(command_prefix="::")

def is_admin(ctx: commands.Context):
    return ctx.author.permissions_in(ctx.channel).administrator

async def send_time_message(ctx, message):
    await ctx.send(message, delete_after=10)

@bot.command(name="hi", help="Checks if alive")
async def answer(ctx: commands.Context):
    response = "Who dis?"
    send_time_message(ctx, response)

@bot.command(name="add", help="Adds to ints")
async def add(ctx: commands.Context, n1: int, n2: int):
    sum = n1 + n2
    response = f"{n1} + {n2} = {sum}"
    send_time_message(ctx, response)

@bot.command(name="summoners", help="Shows who lp-bot is currently tracking")
async def summoners(ctx: commands.Context):
    summoners = json.loads(open("core/DataCollectionStrategy/summoners.json", "r", encoding="utf-8").read())
    response = f"Currently tracking: **{'**, **'.join(summoners[:-1])}** and **{summoners[-1]}**"
    await send_time_message(ctx, response)
    await ctx.message.delete()

@bot.command(name="addSummoner", help="Adds a new summoner to be tracked")
async def add_summoner(ctx: commands.Context, summoner_name: str):
    if is_admin(ctx):
        if is_valid_summoner_name(summoner_name):
            add_summoner_to_pool(summoner_name)
            response = f"{summoner_name} has been added to the pool!\nAn update from the webhooks should occur in <=10 minutes."
        else:
            response = f"Could not find summoner {summoner_name}. Only tracking euw, might that be the problem?"
    else:
        response = f"Need adming privilige."

    await send_time_message(ctx, response)
        

bot.run(TOKEN)