# Object classes from AP core, to represent an entire MultiWorld and this individual World that's part of it
from typing import Any
from worlds.AutoWorld import World
from BaseClasses import MultiWorld, CollectionState, Item, LocationProgressType

# Object classes from Manual -- extending AP core -- representing items and locations that are used in generation
from ..Items import ManualItem
from ..Locations import ManualLocation

# Raw JSON data from the Manual apworld, respectively:
#          data/game.json, data/items.json, data/locations.json, data/regions.json
#
from ..Data import game_table, item_table, location_table, region_table

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value, format_state_prog_items_key, ProgItemsCat, remove_specific_item

# calling logging.info("message") anywhere below in this file will output the message to both console and log file
import logging

########################################################################################
## Order of method calls when the world generates:
##    1. create_regions - Creates regions and locations
##    2. create_items - Creates the item pool
##    3. set_rules - Creates rules for accessing regions and locations
##    4. generate_basic - Runs any post item pool options, like place item/category
##    5. pre_fill - Creates the victory location
##
## The create_item method is used by plando and start_inventory settings to create an item from an item name.
## The fill_slot_data method will be used to send data to the Manual client for later use, like deathlink.
########################################################################################



# Use this function to change the valid filler items to be created to replace item links or starting items.
# Default value is the `filler_item_name` from game.json
def hook_get_filler_item_name(world: World, multiworld: MultiWorld, player: int) -> str | bool:
    return False

def before_generate_early(world: World, multiworld: MultiWorld, player: int) -> None:
    """
    This is the earliest hook called during generation, before anything else is done.
    Use it to check or modify incompatible options, or to set up variables for later use.
    """
    pass

# Called before regions and locations are created. Not clear why you'd want this, but it's here. Victory location is included, but Victory event is not placed yet.
def before_create_regions(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after regions and locations are created, in case you want to see or modify that information. Victory location is included.
def after_create_regions(world: World, multiworld: MultiWorld, player: int):
    # Use this hook to remove locations from the world
    locationNamesToRemove: list[str] = [] # List of location names

    # Add your code here to calculate which locations to remove
    
    # I'm not here to remove locations, I'm here to set them to priority or excluded
    if (is_option_enabled(multiworld, player, "exclude_underworld_lust_chests")):
        for location in multiworld.get_unfilled_locations(player=player):
            if "Angel Bikini Chest" in location.name or "Fire Wings Chest" in location.name:
                location.progress_type = LocationProgressType.EXCLUDED
                
    boss_locations = ["Defeat Myougi in The Floating Keep", "Defeat Pr'gora", "Defeat Electram", "Defeat Amethyst", "Defeat Dark Annihilator", "Defeat Terravine", "Defeat Kratarac", "Defeat Ancient Constructs", "Defeat Myougi in The Library", "Defeat Twin Orcs", "Defeat Azurel"]
    shrine_locations = []
    priority_bosses = world.options.priority_boss_locations.value
    priority_shrines = world.options.priority_shrine_locations.value
    shrine_list = ["Shrine of Lust", "Shrine of Greed", "Shrine of Wrath", "Shrine of Gluttony", "Shrine of Envy", "Shrine of Sloth"]
    gift_list = ["Gift of Lust", "Gift of Greed", "Gift of Wrath", "Gift of Gluttony", "Gift of Envy", "Gift of Sloth"]
    if (is_option_enabled(multiworld, player, "books_of_sin")):
        shrine_locations = gift_list
    else:
        shrine_locations = shrine_list
    
    
    for _ in range(priority_bosses):
        bs = world.random.choice(boss_locations)
        for location in multiworld.get_unfilled_locations(player=player):
            if bs in location.name:
                location.progress_type = LocationProgressType.PRIORITY
        boss_locations.remove(bs)
        
    for _ in range(priority_shrines):
        sh = world.random.choice(shrine_locations)
        for location in multiworld.get_unfilled_locations(player=player):
            if sh in location.name:
                location.progress_type = LocationProgressType.PRIORITY
        shrine_locations.remove(sh)
    
    for region in multiworld.regions:
        if region.player == player:
            for location in list(region.locations):
                if location.name in locationNamesToRemove:
                    region.locations.remove(location)

# This hook allows you to access the item names & counts before the items are created. Use this to increase/decrease the amount of a specific item in the pool
# Valid item_config key/values:
# {"Item Name": 5} <- This will create qty 5 items using all the default settings
# {"Item Name": {"useful": 7}} <- This will create qty 7 items and force them to be classified as useful
# {"Item Name": {"progression": 2, "useful": 1}} <- This will create 3 items, with 2 classified as progression and 1 as useful
# {"Item Name": {0b0110: 5}} <- If you know the special flag for the item classes, you can also define non-standard options. This setup
#       will create 5 items that are the "useful trap" class
# {"Item Name": {ItemClassification.useful: 5}} <- You can also use the classification directly
def before_create_items_all(item_config: dict[str, int|dict], world: World, multiworld: MultiWorld, player: int) -> dict[str, int|dict]:
    return item_config

# The item pool before starting items are processed, in case you want to see the raw item pool at that stage
def before_create_items_starting(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:

    early_memunlocks = ["Aftermath Part 1", "Aftermath Part 2", "Terrestrial Vale Part 1", "Terrestrial Vale Part 2", "Sinister Grotto Part 1", "Sinister Grotto Part 2"]
    starting_memunlock = multiworld.random.choice(early_memunlocks)
    multiworld.local_early_items[player][starting_memunlock] = 1
    
    if (is_option_enabled(multiworld, player, "disable_weapon_logic") and is_option_enabled(multiworld, player, "random_starting_weapon")):
        multiworld.local_early_items[player]["Weapon of Pride"] = 1

    return item_pool

# The item pool after starting items are processed but before filler is added, in case you want to see the raw item pool at that stage
def before_create_items_filler(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    # Use this hook to remove items from the item pool
    itemNamesToRemove: list[str] = [] # List of item names

    # Add your code here to calculate which items to remove.
    #
    # Because multiple copies of an item can exist, you need to add an item name
    # to the list multiple times if you want to remove multiple copies of it.

    for itemName in itemNamesToRemove:
        item = next(i for i in item_pool if i.name == itemName)
        remove_specific_item(item_pool, item)

    # look this is nice and all but i'll add code that moves cosmetics to my start inventory
    # code source: https://github.com/FuzzyGamesOn/Pokemon-TCG-Ages-Manual/blob/main/manual_pokemontcgages_fuzzy/hooks/World.py

    starting_cosmetic_count = world.options.demonic_essence_available.value
    
    if type(starting_cosmetic_count) != int:
        starting_cosmetic_count = 0
        
    # let's calculate how much angelic essence would be added after this hook
    
    total_locations = [l for l in multiworld.get_locations(player=player) if "" in l.name]
    total_items = len(item_pool) - 30 #includes demonic essence so remove that
    angess = len(total_locations) - total_items - 1 #includes victory location so remove that
    
    #print(f"Total locations: {str(len(total_locations)-1)}; item pool: {str(total_items)}")
    
    # Now, whenever a cosmetic would be removed and added to start inventory, if angess > 0, don't do that, instead angess -= 1

    starting_cosmetics = [
        {
            "item_categories": ["Cosmetics"],
            "random": starting_cosmetic_count
        }
    ]

    for starting in starting_cosmetics:
        possible_item_names = []

        for category in starting['item_categories']:
            possible_item_names.extend(
                [
                    name for name, i in world.item_name_to_item.items()
                    if category in i.get("category", [])
                ]
            )

        possible_item_names = set(possible_item_names)

        possible_items = [
            i for i in item_pool
            if i.name in possible_item_names
        ]

        for _ in range(starting['random']):
            if (angess <= 0):
                random_starting_item = world.random.choice(possible_items)
                multiworld.push_precollected(random_starting_item)
                possible_items.remove(random_starting_item)
                item_pool.remove(random_starting_item)
            else:
                angess -= 1

    # okay now remove extras of demonic essence
    essence_to_remove_count = 30 - starting_cosmetic_count

    demess = [
        i for i in item_pool
        if "Demonic Essence" in i.name
    ]

    for _ in range(essence_to_remove_count):
        de = world.random.choice(demess)
        demess.remove(de) # Somehow, this code just worked correctly without this line and I only now realized I should have added it. Better be safe and add it now anyway.
        item_pool.remove(de)

    return item_pool

    # Some other useful hook options:

    ## Place an item at a specific location
    # location = next(l for l in multiworld.get_unfilled_locations(player=player) if l.name == "Location Name")
    # item_to_place = next(i for i in item_pool if i.name == "Item Name")
    # location.place_locked_item(item_to_place)
    # remove_specific_item(item_pool, item_to_place)

# The complete item pool prior to being set for generation is provided here, in case you want to make changes to it
def after_create_items(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    return item_pool

# Called before rules for accessing regions and locations are created. Not clear why you'd want this, but it's here.
def before_set_rules(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after rules for accessing regions and locations are created, in case you want to see or modify that information.
def after_set_rules(world: World, multiworld: MultiWorld, player: int):
    # Use this hook to modify the access rules for a given location

    def Example_Rule(state: CollectionState) -> bool:
        # Calculated rules take a CollectionState object and return a boolean
        # True if the player can access the location
        # CollectionState is defined in BaseClasses
        return True

    ## Common functions:
    # location = world.get_location(location_name, player)
    # location.access_rule = Example_Rule

    ## Combine rules:
    # old_rule = location.access_rule
    # location.access_rule = lambda state: old_rule(state) and Example_Rule(state)
    # OR
    # location.access_rule = lambda state: old_rule(state) or Example_Rule(state)

# The item name to create is provided before the item is created, in case you want to make changes to it
def before_create_item(item_name: str, world: World, multiworld: MultiWorld, player: int) -> str:
    return item_name

# The item that was created is provided after creation, in case you want to modify the item
def after_create_item(item: ManualItem, world: World, multiworld: MultiWorld, player: int) -> ManualItem:
    return item

# This method is run towards the end of pre-generation, before the place_item options have been handled and before AP generation occurs
def before_generate_basic(world: World, multiworld: MultiWorld, player: int):
    if (is_option_enabled(multiworld, player, "books_of_sin")):
        for name in ("Lust", "Greed", "Wrath", "Gluttony", "Envy", "Sloth"):
            item = [i for i in multiworld.get_items() if f"Gift of {name}" in i.name][0]
            location = [l for l in multiworld.get_locations(player=player) if f"Shrine of {name}" in l.name][0]
            location.place_locked_item(item)
            multiworld.itempool.remove(item)

# This method is run at the very end of pre-generation, once the place_item options have been handled and before AP generation occurs
def after_generate_basic(world: World, multiworld: MultiWorld, player: int):
    pass

# This method is run every time an item is added to the state, can be used to modify the value of an item.
# IMPORTANT! Any changes made in this hook must be cancelled/undone in after_remove_item
def after_collect_item(world: World, state: CollectionState, Changed: bool, item: Item):
    # the following let you add to the Potato Item Value count
    # if item.name == "Cooked Potato":
    #     state.prog_items[item.player][format_state_prog_items_key(ProgItemsCat.VALUE, "Potato")] += 1
    pass

# This method is run every time an item is removed from the state, can be used to modify the value of an item.
# IMPORTANT! Any changes made in this hook must be first done in after_collect_item
def after_remove_item(world: World, state: CollectionState, Changed: bool, item: Item):
    # the following let you undo the addition to the Potato Item Value count
    # if item.name == "Cooked Potato":
    #     state.prog_items[item.player][format_state_prog_items_key(ProgItemsCat.VALUE, "Potato")] -= 1
    pass


# This is called before slot data is set and provides an empty dict ({}), in case you want to modify it before Manual does
def before_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data

# This is called after slot data is set and provides the slot data at the time, in case you want to check and modify it after Manual is done with it
def after_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data

# This is called right at the end, in case you want to write stuff to the spoiler log
def before_write_spoiler(world: World, multiworld: MultiWorld, spoiler_handle) -> None:
    pass

# This is called when you want to add information to the hint text
def before_extend_hint_information(hint_data: dict[int, dict[int, str]], world: World, multiworld: MultiWorld, player: int) -> None:

    ### Example way to use this hook:
    # if player not in hint_data:
    #     hint_data.update({player: {}})
    # for location in multiworld.get_locations(player):
    #     if not location.address:
    #         continue
    #
    #     use this section to calculate the hint string
    #
    #     hint_data[player][location.address] = hint_string

    pass

def after_extend_hint_information(hint_data: dict[int, dict[int, str]], world: World, multiworld: MultiWorld, player: int) -> None:
    pass

def hook_interpret_slot_data(world: World, player: int, slot_data: dict[str, Any]) -> dict[str, Any]:
    """
        Called when Universal Tracker wants to perform a fake generation
        Use this if you want to use or modify the slot_data for passed into re_gen_passthrough
    """
    return slot_data
