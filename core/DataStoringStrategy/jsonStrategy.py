import json
import random

sad_word_pool = [
        "jesus fucking christ",
        "bloody norah",
        "flaming nora",
        "bloody nora",
        "oh shit",
        "i'll be a son of a bitch",
        "bollocks to it",
        "shit fire and save matches",
        "jesus fuck",
        "fuck you",
        "fucking shit",
        "jesus fucking",
        "holy fuck",
        "holy shit",
        "fucking hell",
        "holy fuck knuckles",
        "i'll be dipped in shit",
        "fuck me",
        "holy crap",
        "shit",
        "shite",
        "bugger",
        "crap",
        "sucky",
        "sucks",
        "fucking",
        "fark",
        "fook",
        "motherfucking",
        "pissing",
        "goddammit",
        "goddamn",
        "godammit",
        "oh my fucking god",
        "omfg",
        "god dammit",
        "well that sucks",
        "this sucks"    
    ]   

happy_word_pool = [
    "cool",
    "nice",
    "unbelievable"
]

tier_stats = {
    "IRON": 1,
    "BRONZE": 2,
    "SILVER": 3,
    "GOLD": 4,
    "PLATINUM": 5,
    "DIAMOND": 6,
    "MASTER": 7
}

rank_stats = {
    "I": 1,
    "II": 2,
    "III": 3,
    "IV": 4
}

# Either soloduo or flex, same layout
def create_new_cat_data(c):
    return {
        "tier": c["tier"],
        "rank": c["rank"],
        "lp": c["leaguePoints"],
        "wins": c["wins"],
        "losses": c["losses"]
    }

def create_new_summoner_entry(summoner) -> dict:
    return {
        "soloduo": create_new_cat_data(summoner["soloduo"]),
        "flex": create_new_cat_data(summoner["flex"])
    }

def generate_message(value_change):
    if value_change > 0:
        return (random.choice(happy_word_pool) + " {} rose to {}")
    else:
        return random.choice(sad_word_pool) + "{} fell to {}"

def calc_difference(old_rank, new_rank, name):
    try:
        tier_dif = tier_stats[new_rank["tier"]] - tier_stats[old_rank["tier"]]
        rank_dif = rank_stats[new_rank["rank"]] - rank_stats[old_rank["rank"]]
        lp_dif = int(new_rank["leaguePoints"]) - int(old_rank["lp"])
    except:
        print(old_rank, new_rank, name)
    if tier_dif < 0 or rank_dif < 0 or lp_dif < 0:
        message =  generate_message(-1).format(name, f"{new_rank['tier']} {new_rank['rank']} {new_rank['leaguePoints']}")
        return (True, message)
    elif tier_dif > 0 or rank_dif > 0 or lp_dif > 0:
        message = generate_message(1).format(name, f"{new_rank['tier']} {new_rank['rank']} {new_rank['leaguePoints']}")
        return (True, message)
    else:
        return (False, "")

def check_if_updated(summoner: dict, summoner_data: dict, queue_type: str) -> (bool, str):
    new_rank = summoner[queue_type]
    old_rank = summoner_data[summoner["name"]][queue_type]

    return calc_difference(old_rank, new_rank, summoner["name"])

# Returns (New summoners, soloduo-update, flex-update)
def update_stats(updated_summoners: list) -> list:
    try:
        summoner_data = json.loads(open("core/DataStoringStrategy/summoners_data.json", "r").read())
    except:
        summoner_data = {}

    messages = []

    for summoner in updated_summoners:
        name = summoner["name"]

        if name not in summoner_data:
            summoner_data[name] = create_new_summoner_entry(summoner)
            message = f"Welcome {name}. May your rank forever rise!"
            messages.append(message)
            pass
        
        duo_changed, duo_message = check_if_updated(summoner, summoner_data, "soloduo")
        flex_changed, flex_message = check_if_updated(summoner, summoner_data, "flex")

        if duo_changed:
            summoner_data[name]["solduo"] = create_new_cat_data(summoner["soloduo"])
            messages.append(duo_message)
        if flex_changed:
            summoner_data[name]["flex"] = create_new_cat_data(summoner["flex"])
            messages.append(flex_message)
        
    with open("core/DataStoringStrategy/summoners_data.json", "w") as f:
        json.dump(summoner_data, f)
        print("saved")

    return messages

if __name__ == "__main__":
    update_stats({})