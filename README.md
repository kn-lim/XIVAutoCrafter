# FFXIV AutoCrafter

Automatically activates multiple crafting macros using [pynput](https://pypi.org/project/pynput/) while refreshing food and potion buffs.

## Quick Start

```
$ python3 autocrafter.py -h
usage: autocrafter.py [-h] [-v] [-f FOOD] [--food_duration {30,40,45}] [-p POTION] [-m2 MACRO2] [--macro2_duration MACRO2_DURATION]
                      delay max_amount macro1 macro1_duration confirm cancel start_stop stop

positional arguments:
  delay                 sets delay per craft
  max_amount            maximum amount to craft
  macro1                macro 1 hotkey
  macro1_duration       macro 1 duration
  confirm               confirm hotkey
  cancel                cancel hotkey
  start_stop            start/stop hotkey
  stop                  stop hotkey

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity
  -f FOOD, --food FOOD  use food option and hotkey
  --food_duration {30,40,45}
                        duration of food in minutes
  -p POTION, --potion POTION
                        use potion option and hotkey
  -m2 MACRO2, --macro2 MACRO2
                        macro 2 hotkey
  --macro2_duration MACRO2_DURATION
                        macro 2 duration
```

Time is measured in seconds.

## TODO

- GUI