from wowapi import WowApi
import requests
from pprint import pprint
import time # To test the response speed of WoW API
import json

# Constants
WOW_API_KEY = "3t5pc8m8ku57q8wgve9axkeppp6qvp6z"
GUILD_RANKS = {0: "Guild Master",
               1: "Officer",
               2: "Officer Alt",
               3: "Veteran",
               4: "Senior Raider",
               5: "Raider",
               6: "Raider Alt",
               7: "Trial",
               8: "Social",
               9: "Yamcha"}

CLASS_DICT =  {1: "Warrior",
               2: "Paladin",
               3: "Hunter",
               4: "Rogue",
               5: "Priest",
               6: "Death Knight",
               7: "Shaman",
               8: "Mage",
               9: "Warlock",
               10: "Monk",
               11: "Druid",
               12: "Demon Hunter"}

RAIDER_RANKS = [0, 1, 3, 4, 5, 7]

def get_guild_members():
    dict = requests.get("https://us.api.battle.net/wow/guild/Emerald%20Dream/Suboptimal?fields=members,talents&locale=en_US&apikey=" + WOW_API_KEY).json()

    w_dict = {}

    for member in dict["members"]:
        name = member["character"]["name"]
        #print(member)
        #print("https://us.api.battle.net/wow/character/Emerald%20Dream/" + member["character"]["name"] + "?fields=talents?locale=en_US&apikey=" + WOW_API_KEY)
        member_dict = requests.get("https://us.api.battle.net/wow/character/Emerald%20Dream/" + name + "?fields=talents&?locale=en_US&apikey=" + WOW_API_KEY).json()
        #print(member_dict)
        if member["rank"] in RAIDER_RANKS:
            w_dict[name] = {}
            w_dict[name]["class"] = CLASS_DICT[member_dict["class"]]
            #print(name)
            #print(member_dict["talents"])
            for spec in member_dict["talents"]:
                if "selected" in spec:
                    w_dict[name]["spec"] = spec["spec"]["name"]
            w_dict[name]["rank"] = GUILD_RANKS[member["rank"]]
            print(w_dict[name])

    with open('guild_roster.json', 'w') as f:
        json.dump(w_dict, f)

if __name__ == "__main__":
    start_time = time.time()
    get_guild_members()
    end_time = time.time()

    print(end_time - start_time)
