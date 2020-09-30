# bot.py
# Client handling updates to discord

import os

from discord.ext import commands
from dotenv import load_dotenv

from core.DataStoringStrategy import postgresStrategy
from core.DataCollectionStrategy import is_valid_summoner_name
import update

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

bot = commands.Bot(command_prefix="::")


def is_admin(ctx: commands.Context):
    return ctx.author.permissions_in(ctx.channel).administrator


async def send_time_message(ctx, message):

    await ctx.send(message, delete_after=10)
    await ctx.message.delete()


@bot.command(name="hi", help="Checks if alive")
async def answer(ctx: commands.Context):
    response = "Who dis?"
    await send_time_message(ctx, response)


@bot.command(name="add", help="Adds to ints")
async def add(ctx: commands.Context, n1: int, n2: int):
    sum = n1 + n2
    response = f"{n1} + {n2} = {sum}"
    await send_time_message(ctx, response)


@bot.command(name="summoners", help="Shows summoners")
async def summoners(ctx: commands.Context, ):
    summoners = postgresStrategy.get_summoners()
    response = f"summoners {summoners}"
    await send_time_message(ctx, response)


@bot.command(name="stats", help="Shows all stats")
async def stats(ctx: commands.Context, ):
    stats = postgresStrategy.get_recent_flex_stats()
    soloduo_stats = postgresStrategy.get_recent_soloduo_stats()

    for summ in stats:
        if summ in soloduo_stats:
            stats[summ].update(soloduo_stats[summ])
            soloduo_stats.pop(summ)
    stats.update(soloduo_stats)

    message = ""
    for summoner in stats:
        message += f"*{summoner}*: {stats[summoner]}\n"

    await send_time_message(ctx, message)

@bot.command(name="addSummoner", help="Adds summoner to watch")
async def addSummoner(ctx: commands.Context, summoner_name: str):
    if is_admin(ctx):
        summoner = is_valid_summoner_name(summoner_name)
        if summoner:
            postgresStrategy.insert_new_summoner(summoner["name"])
            await send_time_message(ctx, f"{summoner['name']} added to summoner pool.")
        else:
            await send_time_message(ctx, f"{summoner_name} is not a valid name on euw1")
    else:
        await send_time_message(ctx, "Not admin")

@bot.command(name="removeSummoner", help="Removes summoner from pool")
async def remove_summoner(ctx: commands.Context, summoner_name: str):
    if is_admin(ctx):
        postgresStrategy.delete_summoner(summoner_name)
        await send_time_message(ctx, f"Removed {summoner_name}")
    else:
        await send_time_message(ctx, "Not admin")

bot.run(TOKEN)
