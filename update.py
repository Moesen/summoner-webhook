import os
from dotenv import load_dotenv
import random

from discord_webhook import DiscordWebhook, DiscordEmbed

from core.DataCollectionStrategy import get_stats_for_all
from core.DataStoringStrategy import update_stats

load_dotenv()
webhook_url = os.getenv("WEBHOOK_URL")

stats = get_stats_for_all()
announcements = update_stats(stats)
if len(announcements) > 0:
    webhook = DiscordWebhook(url=webhook_url, username="LP-Tracker")

    embed = DiscordEmbed( color=242424)
    embed.set_author(name="LP-tracker", url="https://github.com/Moesen/summoner-webhook/")
    webhook.add_embed(embed)
    
    for idx, message in enumerate(announcements):
        color = random.randint(0, 999999)
        em = DiscordEmbed(title = message, color=color)
        webhook.add_embed(em)

    response = webhook.execute()
