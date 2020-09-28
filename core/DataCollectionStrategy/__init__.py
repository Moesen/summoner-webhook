import os

from riotwatcher import LolWatcher, ApiError
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("RIOT_API_KEY")


def get_stats(summoner_name: str) -> dict:
    watcher = LolWatcher(api_key)
    my_region = "euw1"

    me = watcher.summoner.by_name(my_region, summoner_name)
    my_stats = watcher.league.by_summoner(my_region, me['id'])

    return {**me, **{"flex": my_stats[0]}, **{"soloduo": my_stats[1]}}

def get_stats_for_all() -> dict:
    names = [
        "Kongsnooze", 
        "Dr Røvkløe"
    ]
    return [get_stats(name) for name in names]

if __name__ == "__main__":
    print(get_stats("Kongsnooze"))