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
    flex, soloduo = None, None

    if len(my_stats) > 0:
        flex = next(x for x in my_stats if "queueType" in x.keys() and x["queueType"] == "RANKED_FLEX_SR")
        soloduo = next(x for x in my_stats if "queueType" in x.keys() and x["queueType"] == "RANKED_SOLO_5x5")

    return {**me, **{"flex": flex}, **{"soloduo": soloduo}}

def get_stats_for_all(summoners: list) -> dict:
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

def add_summoner_to_pool(summoner_name: str):
    path = "core/DataCollectionStrategy/summoners.json"
    summoners = json.loads(open(path, "r", encoding="utf-8").read())
    summoners = list({*summoners, summoner_name})
    with open(path, "w", encoding="utf-8") as fb:
        json.dump(summoners, fb)

if __name__ == "__main__":
    print(get_stats("Kongsnooze"))