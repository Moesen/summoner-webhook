import os
from dotenv import load_dotenv
import random

from discord_webhook import DiscordWebhook, DiscordEmbed

from core.DataCollectionStrategy import get_stats_for_all
from core.DataStoringStrategy import postgresStrategy

load_dotenv()
webhook_url = os.getenv("WEBHOOK_URL")


def clean_stats(stats: list) -> dict:
    cleaned_stats = {}
    for stat in stats:
        summoner_name = stat["name"]
        flex = {
            "tier": stat["flex"]["tier"],
            "rank": stat["flex"]["rank"],
            "lp": stat["flex"]["leaguePoints"]
        }
        soloduo = {
            "tier": stat["soloduo"]["tier"],
            "rank": stat["soloduo"]["rank"],
            "lp": stat["soloduo"]["leaguePoints"]
        }
        cleaned_stats[summoner_name] = {"flex": flex, "soloduo": soloduo}

    return cleaned_stats


def is_equal(new, recent):
    return new["tier"] == recent["tier"] and new["rank"] == recent["rank"] and new["lp"] == recent["lp"]


def compare_changes(new, recent_flex, recent_soloduo) -> (list, list):
    changed_flex, changed_soloduo = [], []


    # Checking if have ever been updated
    for summoner, new_stats in new.items():
        if summoner not in recent_flex or not is_equal(new_stats["flex"], recent_flex[summoner]):
            changed_flex.append({"summoner_name": summoner, **new_stats["flex"]})
        if summoner not in recent_soloduo or not is_equal(new_stats["soloduo"], recent_soloduo[summoner]):
            changed_soloduo.append({"summoner_name": summoner, **new_stats["soloduo"]})
    return changed_soloduo, changed_flex


def check_for_updates(stats: list) -> dict:
    cleaned_stats = clean_stats(stats)
    recent_flex = postgresStrategy.get_recent_flex_stats()
    recent_soloduo = postgresStrategy.get_recent_soloduo_stats()

    changed_soloduo, changed_flex = compare_changes(cleaned_stats, recent_flex, recent_soloduo)

    return {"flex": changed_flex, "soloduo": changed_soloduo}


def insert_updated_stats_to_db(update_stats: dict):
    insertable_flex = [(x["tier"], x["rank"], x["lp"], x["summoner_name"]) for x in update_stats["flex"]]
    insertable_soloduo = [(x["tier"], x["rank"], x["lp"], x["summoner_name"]) for x in update_stats["soloduo"]]

    if len(insertable_flex) > 0:
        postgresStrategy.insert_new_flex_stats(insertable_flex)
    if len(insertable_soloduo) > 0:
        postgresStrategy.insert_new_soloduo_stats(insertable_soloduo)


def make_announcements(update_stats: dict) -> list:
    for update in update_stats["flex"]:
        print(update)
    for update in update_stats["soloduo"]:
        print(update)


postgresStrategy.insert_new_flex_stats([("123", "123", 123, "KongSnooze")])
summoners = postgresStrategy.get_summoners()
stats = get_stats_for_all(summoners)
updated_stats = check_for_updates(stats)
insert_updated_stats_to_db(updated_stats)
announcements = make_announcements(updated_stats)

# if len(announcements) > 0:
#     webhook = DiscordWebhook(url=webhook_url, username="LP-Tracker")
#
#     for idx, message in enumerate(announcements):
#         color = random.randint(0, 999999)
#         em = DiscordEmbed(title = message, color=color)
#         webhook.add_embed(em)
#
#     response = webhook.execute()
