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

Run `pip3 install -r requirements.txt` to install the requirements.

## Usage

Run `python3 xivautocrafter.py` to launch XIVAutoCrafter.

```
Required Arguments:
  Start/Pause                  Start/Pause Program Hotkey
  Stop                         Stop Program Hotkey
  Max Amount                   Maximum Amount to Craft
  Macro 1                      Macro 1 Hotkey
  Macro 1 Duration             Macro 1 Duration in Seconds
  Confirm                      Confirm Hotkey
  Cancel                       Cancel Hotkey

Optional Arguments:
  Verbose                      Increase Output Verbosity
  Macro 2                      Macro 2 Hotkey
  Macro 2 Duration             Macro 2 Duration in Seconds
  Food                         Food Hotkey
  Food Duration {30,40,45}     Food Duration in Minutes
  Potion                       Potion Hotkey
```

## Prepping the Game

In order for XIVAutoCrafter to work properly:

1. **Make sure you are not near anything that can be interacted with.**
    - This is important to make sure you don't accidentally target something else and thus being unable to craft.
2. **Open the Crafting Log and select the item you want to craft with XIVAutoCrafter.**
    - To ensure your character is in the correct state, start and then cancel the craft without any additional inputs.

Once that is done, press the _Start/Pause XIVAutoCrafter_ hotkey to start the tool.

## Accepted Keys

- Alphanumeric
- Insert, Delete, Home, End, Page Up, Page Down

# FAQ

- **Does the game need to be in focus?**
    - Yes.

# TODO

- Sanitize user input properly
- More supported hotkeys
- Show estimated time to complete the craft
- Game no longer needs to be in focus
- Allow switching crafts while remembering current food and potion duration
