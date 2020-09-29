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
    await send_time_message(ctx, response)

@bot.command(name="add", help="Adds to ints")
async def add(ctx: commands.Context, n1: int, n2: int):
    sum = n1 + n2
    response = f"{n1} + {n2} = {sum}"
    await send_time_message(ctx, response)



bot.run(TOKEN)