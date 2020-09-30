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
    return_dict = {**me}

    if len(my_stats) > 0:

        flex = list(x for x in my_stats if "queueType" in x.keys() and x["queueType"] == "RANKED_FLEX_SR")
        soloduo = list([x for x in my_stats if "queueType" in x.keys() and x["queueType"] == "RANKED_SOLO_5x5"])
        if flex:
            return_dict["flex"] = flex[0]
        if soloduo:
            return_dict["soloduo"] = soloduo[0]

    return return_dict


def get_stats_for_all(summoners: list) -> list:
    return [get_stats(summoner_name) for summoner_name in summoners]


def is_valid_summoner_name(summoner_name: str) -> LolWatcher.summoner:
    watcher = LolWatcher(api_key)
    region = "euw1"

    try:
        summoner = watcher.summoner.by_name(region, summoner_name)
        return summoner
    except ApiError as err:
        return False
    except Exception as exc:
        with open("logs.txt", "a", encoding="utf-8") as f:
            f.write(f"{time.localtime()}: {exc.message}")
        return False

if __name__ == "__main__":
    print(get_stats("Kongsnooze"))
