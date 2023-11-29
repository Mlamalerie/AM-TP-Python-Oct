import csv
from math import sqrt,floor
from typing import List

pokedex_file_path = 'Pokemon.csv'

def parse_pokedex(file_path : str) -> List[dict]:
    with open(file_path, 'r') as file:
        my_reader = csv.reader(file, delimiter=';')
        keys = next(my_reader)
        results = [dict(zip(keys,row)) for row in my_reader]
    return results

pokemons_list = parse_pokedex(pokedex_file_path)
print(f"Combien y'a t'il de Pokémon ref ? -> {len(pokemons_list)}")
def count_type(pokemons : List[dict] , what_type : str):
    return sum(1 for pokemon in pokemons if pokemon["Type 1"] == what_type)

def count_legendary(pokemons : List[dict]) -> int:
    return sum(1 for pokemon in pokemons if pokemon["Legendary"] == "True")

print(f"Combien de Pokémons sont de type Plante ? -> {count_type(pokemons_list,'Grass')}")
print(f"Combien sont légendaires ? -> {count_legendary(pokemons_list)}")


def update_pokemons_stats(pokemons : List[dict]) -> List[dict]:

    for pokemon in pokemons:
        # Puissance
        hp,attack,def_ = int(pokemon["HP base"]), int(pokemon["Attack base"]), int(pokemon["Defense base"])
        spe_attack,spe_def,speed = int(pokemon["Sp. Atk base"]),int(pokemon["Sp. Def base"]),int(pokemon["Speed base"])
        pokemon["Puissance Totale"] = hp + attack + def_ + spe_attack + spe_def  + speed

        speed_multi = 1 + (speed - 75) / 500


        pokemon["CP"] = floor((sqrt(hp) * attack * sqrt(def_))/100)
        pokemon["HP GO"] = int(50 + 1.75 * hp)
        pokemon["Attack GO"] = int((0.25 * min(attack,spe_attack) + (7/4) * max(attack,spe_attack)) * speed_multi)
        pokemon["Defense GO"] = int((0.75 * min(def_,spe_def) + (5/4) * max(def_,spe_def)) * speed_multi)
    return pokemons

def get_best_pokemon(pokemons : List[dict]) -> dict:
    sorted_pokemons = sorted(pokemons, key=lambda x: x["Puissance Totale"])
    return sorted_pokemons[-1]


pokemons_list = update_pokemons_stats(pokemons_list)
best_pokemon = get_best_pokemon(pokemons_list)
print(f"Quel est le Pokémon le plus puissant ? -> {best_pokemon['Name']} ({best_pokemon['Puissance Totale']})")

def save_new_pokedex(pokemons : List[dict]) -> None:

    file_path = "Pokemon-processed.csv"
    try:
        keys = pokemons[0].keys()
        with open(file_path, 'w') as output_file:
            dict_writer = csv.DictWriter(output_file, keys,delimiter=";")
            dict_writer.writeheader()
            dict_writer.writerows(pokemons)

    except:
        print("*error save*")
    else:
        print(f"*saved at {file_path}*")


save_new_pokedex(pokemons_list)