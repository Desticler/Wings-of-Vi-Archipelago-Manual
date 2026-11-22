# Wings of Vi Archipelago Manual
Archipelago Manual implementation for [Wings of Vi](https://store.steampowered.com/app/318530/Wings_of_Vi/), a 2D action platformer developed by Grynsoft.

# Manual Rules
You're expected to play on an endgame savefile where the Purified modifier was picked at the beginning to start with all weapons, and the game was completed with no optional items collected & minimal achievements unlocked (Only the ones for defeating bosses & having all weapons). An Angel mode savefile meeting this criteria is provided in the releases, with more valid saves potentially coming later.

You start in **The Floating Keep - Current time**, with the Darkheim Watch letting you travel to **The Floating Keep - Sleeping memory**. From there, you're only allowed to travel to other areas if you have their respective **Memory Unlock**. Most Memory Unlocks unlock 2 memories - an area and a boss. For example, **Aftermath Part 1** unlocks **Aftermath - Portal memory** and **Aftermath - Myougi memory**. The one exception is **The Acropolis of Anguish** Memory Unlock, which only unlocks one memory - **The Acropolis of Anguish - Gate memory**.

Additionally, while you have access to all 7 weapons from the start, you're only allowed to use weapons you received as items from the multiworld. Some locations may show up in the Manual client as out-of-logic if you do not have certain weapons, but aside from **Angel Bikini Chest** and **Fire Wings Chest** requiring **Weapon of Lust**, as well as the final boss requiring **Weapon of Pride**, these are merely suggestions to prevent unreasonable situations. If you have the Memory Unlock, you are allowed to do the area and boss it unlocks fully!

The goal of the manual is to unlock Heart of the Baneful by collecting enough Demonic Essence, Memory Unlocks and Weapons - the exact amounts are set by the player in options - and then defeat Jeh'Oul and Supreme Jeh'Oul.

# Locations
- Opening every secret chest

- Collecting every food pickup

- Visiting every Sin Shrine

- Defeating every boss

- (optionally) Unlocking every non-flawless achievement

- (optionally) Unlocking every flawless achievement

- (optionally) Opening every endgame potion chest available on your difficulty

- (optionally) Collecting the keys in the second half of The Underworld

# Items
- Memory Unlocks

- Weapons

- Cosmetics

- (optionally) Demonic Essence, macguffin items needed to unlock Heart of the Baneful

- (optionally) Books of Sin, items needed to get items from Sin Shrines

# Options

**Random Starting Weapon** - Randomizes which weapon is unlocked from the start. If disabled, you start with Weapon of Pride. Because weapon logic isn't implemented yet, enabling this option will make Weapon of Pride local and early. Once weapon logic is implemented, this will remain as failsafe behavior in case weapon logic is disabled but random starting weapon is enabled. (default: false)

**Demonic Essence Available** - How much Demonic Essence is added to the pool. If a Demonic Essence would replace a random cosmetic, said cosmetic is instead added to your starting inventory. (default: 15)

**Demonic Essence Required** - How much Demonic Essence is needed to unlock Heart of the Baneful. This is a percentage. So, for example, if you set Demonic Essence Available to 15 and Demonic Essence Required to 80, you'll need 12 Demonic Essence. (default: 80)

**Memory Unlocks Required** - How many Memory Unlocks are needed to unlock Heart of the Baneful. (default: 1)

**Weapons Required** - How many Weapons are needed to unlock Heart of the Baneful. (default: 1)

**Priority Boss Locations** - How many bosses (other than Jeh'Oul and Supreme Jeh'Oul) will be guaranteed to hold progression or useful items. (default: 4)

**Priority Shrine Locations** - How many Sin Shrines (or their respective Shrine Gifts) will be guaranteed to hold progression or useful items. (default: 2)

**Exclude Heart of the Baneful** - Prevents Heart of the Baneful locations from having progression or useful items. Note that even with this option disabled, your own progression items will never be in Heart of the Baneful. (default: false)

**Include Achievements** - Adds non-flawless achievements as locations and adds the cosmetics you get for them as filler items. (default: true)

**Include Flawless Achievements** - Adds flawless achievements as locations and adds the cosmetics you get for them as filler items. (default: false)

**Books of Sin** - Replaces the 3 food items with Books of Sin. You will need all 3 books to receive Sin Shrine items. To reduce backtracking, you may still interact with Sin Shrines before having all 3 books. Doing so will grant you their Shrine Gift. Then, once you have all 3 books, you may unlock all your obtained Shrine Gifts all at once. (default: true)

**Include Endgame Potions** - Adds the endgame potion chests as locations and their respective potions as filler items. 4 options, one for completely disabling the setting and 3 for each of the difficulties. If Hothead Potion and/or Masochist Potion chests are included, they additionally require having all 7 weapons. (default: disabled)

**Include Underworld Keys** - Adds locations for the 4 keys found during Portal memory of The Underworld. This aims to address the fact that normally, Portal memory is a pretty challenging section of the game with only one location near its end. (default: true)

**Exclude Underworld Lust Chests** - Ensures that Angel Bikini Chest and Fire Wings Chest locations will not have progression or useful items. These two chests are both near the end of their respective areas and require Weapon of Lust, resulting in very tedious backtracking.

**Prehint Flawless Achievements** - Prehints flawless achievement locations, if they're included. This is a temporary option that will be replaced with the scoutable locations feature once it's supported by the latest stable Manual client.
