import os
import json

import time

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
    summoners = json.loads(open("core/DataCollectionStrategy/summoners.json", "r", encoding="utf-8").read())
    return [get_stats(summoner_name) for summoner_name in summoners]

def is_valid_summoner_name(summoner_name: str) -> bool:
    watcher = LolWatcher(api_key)
    region = "euw1"

    
    try:
        summoner = watcher.summoner.by_name(region, summoner_name)
        return True
    except ApiError as err:
        return False
    except Exception as exc:
        with open("logs.txt", "a", encoding="utf-8") as f:
            f.write(f"{time.localtime()}: {exc.message}")
        return False

if __name__ == "__main__":
    is_valid_summoner_name("Kongsnoze")