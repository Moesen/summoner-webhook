# bot.py
# Client handling updates to discord

import os

from discord.ext import commands
from dotenv import load_dotenv

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

bot.run(TOKEN)