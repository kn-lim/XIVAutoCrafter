<p align="center">
    <img alt="XIVAutoCrafter" width=256 height=256 src="https://raw.githubusercontent.com/kn-lim/XIVAutoCrafter/master/images/program_icon.png" />
</p>

# XIVAutoCrafter - A FFXIV Automated Crafting Tool

Automatically activates multiple crafting macros using [pynput](https://pypi.org/project/pynput/) while refreshing food and potion buffs.

GUI provided by [Gooey](https://github.com/chriskiehl/Gooey).

Supports FFXIV Endwalker Patch 6.05+.

## Requirements

| Name | Version |
|------|---------|
| Python | >= 3.8 |
| pynput | >= 1.7 |
| Gooey | >= 1.0 |

# Using the Tool

## Installation

Run `pip3 install -r requirements.txt` to install pynput and Gooey.

## Usage

Run `python3 xivautocrafter.py` to launch XIVAutoCrafter.

```
required arguments:
  delay                      sets delay per craft
  max_amount                 maximum amount to craft
  macro1                     macro 1 hotkey
  macro1_duration            macro 1 duration in seconds
  confirm                    confirm hotkey
  cancel                     cancel hotkey
  start_pause                start/pause XIVAutoCrafter hotkey
  stop                       stop XIVAutoCrafter hotkey

optional arguments:
  verbose                    increase output verbosity
  food                       use food option and hotkey
  food_duration {30,40,45}   duration of food in minutes
  potion                     use potion option and hotkey
  macro2                     macro 2 hotkey
  macro2_duration            macro 2 duration in seconds
```

## Prepping the Game

In order for XIVAutoCrafter to work properly:

1. **Make sure you are not near anything that can be interacted with.**
    - This is important to make sure you don't accidentally target something else and thus being unable to craft.
2. **Open the Crafting Log and select the item you want to craft with XIVAutoCrafter.**
    - To ensure your character is in the correct state, start and then cancel the craft without any additional inputs.

Once that is done, press the _Start/Pause XIVAutoCrafter_ hotkey to start the tool.

## Accepted Special Hotkeys

| Name | Value |
|------|-------|
| Insert | `insert` |
| Delete | `delete` |
| Home | `home` |
| End | `end` |
| Page Up | `page_up` |
| Page Down | `page_down` |

# FAQ

- **Does the game need to be in focus?**
    - Yes.

# TODO

- Sanitize user input properly
- More supported hotkeys
- Show estimated time to complete the craft
- Game no longer needs to be in focus
- Allow switching crafts while remembering current food and potion duration
