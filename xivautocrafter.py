import time
import threading
from pynput.keyboard import Key, KeyCode, Controller, Listener
from gooey import Gooey, GooeyParser

from src.keys import *

# Constants
VERSION = "v1.1.0"
COPYRIGHT = "2022"

DELAY = 1.5
CONSUMABLE_DELAY = 2
KEY_DELAY = 0.3

POTION_DURATION = 900


class XIVAutoCrafter(threading.Thread):
    def __init__(
        self,
        max_amount,
        macro1,
        macro1_duration,
        confirm,
        cancel,
        start_pause,
        stop,
        food=None,
        food_duration=None,
        potion=None,
        macro2=None,
        macro2_duration=None,
        debug=False,
    ):
        super().__init__()
        self.debug = debug
        self.running = False
        self.program_running = True

        self.food = food
        self.food_duration = food_duration
        self.potion = potion
        self.max_amount = max_amount
        self.macro1 = macro1
        self.macro1_duration = macro1_duration
        self.macro2 = macro2
        self.macro2_duration = macro2_duration
        self.confirm = confirm
        self.cancel = cancel
        self.start_pause = start_pause
        self.stop = stop

        self.start_food_time = None
        self.start_potion_time = None
        self.counter = 0

    def start_autocrafter(self):
        if self.debug:
            print("STARTING AUTOCRAFTER")

        self.running = True

    def stop_autocrafter(self):
        if self.debug:
            print("\nPAUSING AUTOCRAFTER\n")

        self.running = False

    def exit(self):
        self.stop_autocrafter()

        if self.debug:
            print("\nEXITING AUTOCRAFTER\n")

        self.program_running = False

    def start_craft(self):
        keyboard.tap(self.confirm)
        time.sleep(KEY_DELAY)
        keyboard.tap(self.confirm)
        time.sleep(KEY_DELAY)
        keyboard.tap(self.confirm)
        time.sleep(KEY_DELAY)
        time.sleep(DELAY)

    def cancel_craft(self):
        keyboard.tap(self.confirm)
        time.sleep(KEY_DELAY)
        keyboard.tap(self.cancel)
        time.sleep(KEY_DELAY)
        keyboard.tap(self.confirm)
        time.sleep(KEY_DELAY)
        time.sleep(DELAY)

    def check_food(self):
        if self.debug:
            print("CHECKING FOOD")

        if self.start_food_time is not None:
            difference = int(time.time()) - self.start_food_time

            if self.debug:
                print(f"FOOD DURATION: {difference} / {self.food_duration}")

            if difference > self.food_duration:
                self.consume_food()

        else:
            self.consume_food()

    def consume_food(self):
        if self.debug:
            print("CONSUMING FOOD")

        self.cancel_craft()

        self.start_food_time = int(time.time())
        keyboard.tap(self.food)
        time.sleep(CONSUMABLE_DELAY)

        self.start_craft()

    def check_potion(self):
        if self.debug:
            print("CHECKING POTION")

        if self.start_potion_time is not None:
            difference = int(time.time()) - self.start_potion_time

            if self.debug:
                print(f"POTION DURATION: {difference} / {POTION_DURATION}")

            if difference > POTION_DURATION:
                self.consume_potion()

        else:
            self.consume_potion()

    def consume_potion(self):
        if self.debug:
            print("CONSUMING POTION")

        self.cancel_craft()

        self.start_potion_time = int(time.time())
        keyboard.tap(self.potion)
        time.sleep(CONSUMABLE_DELAY)

        self.start_craft()

    def run(self):
        while self.program_running:
            while self.running:
                self.start_craft()

                if self.food is not None:
                    self.check_food()

                if self.potion is not None:
                    self.check_potion()

                keyboard.tap(self.macro1)
                time.sleep(self.macro1_duration)

                if self.macro2 is not None:
                    keyboard.tap(self.macro2)
                    time.sleep(self.macro2_duration)

                self.counter += 1
                print(f"CRAFTED: {self.counter} / {self.max_amount}\n")
                if self.counter >= self.max_amount:
                    self.exit()

                time.sleep(DELAY)

            time.sleep(DELAY)


def str_to_key(string):
    if len(string) == 1:
        key = KeyCode(char=string.lower())

    else:
        key = SPECIAL_KEYS[string]

    return key


@Gooey(
    program_name="XIVAutoCrafter",
    program_description="A FFXIV Automated Crafting Tool",
    image_dir="images",
    menu=[
        {
            "name": "File",
            "items": [
                {
                    "type": "AboutDialog",
                    "menuTitle": "About",
                    "name": "XIVAutoCrafter",
                    "description": "A FFXIV Automated Crafting Tool",
                    "version": VERSION,
                    "copyright": COPYRIGHT,
                    "website": "https://github.com/kn-lim/XIVAutoCrafter",
                    "license": "MIT",
                }
            ],
        }
    ],
    progress_regex=r"^CRAFTED: (\d+) / (\d+)",
    progress_expr="x[0] / x[1] * 100",
)
def main():
    parser = GooeyParser()

    # Config
    config = parser.add_argument_group("XIVAutoCrafter Config")
    config.add_argument(
        "start_pause",
        metavar="Start/Pause",
        help="Start/Pause Program Hotkey",
        choices=KEYS + [*SPECIAL_KEYS],
        type=str,
        widget="FilterableDropdown",
        gooey_options={"placeholder": "Enter Key"},
    )
    config.add_argument(
        "stop",
        metavar="Stop",
        help="Stop Program Hotkey",
        choices=KEYS + [*SPECIAL_KEYS],
        type=str,
        widget="FilterableDropdown",
        gooey_options={"placeholder": "Enter Key"},
    )
    config.add_argument(
        "--max_amount",
        metavar="Max Amount",
        help="Maximum Amount to Craft",
        type=int,
        default=0,
        widget="IntegerField",
        gooey_options={"min": 1, "max": 99, "increment": 1},
    )
    config.add_argument(
        "--verbose",
        metavar="Verbose",
        action="store_true",
        help="Increase Output Verbosity",
        widget="BlockCheckbox",
    )

    # Macros
    macros = parser.add_argument_group("Macros")
    macros.add_argument(
        "macro1",
        metavar="Macro 1",
        help="Macro 1 Hotkey",
        choices=KEYS + [*SPECIAL_KEYS],
        type=str,
        widget="FilterableDropdown",
        gooey_options={"placeholder": "Enter Key"},
    )
    macros.add_argument(
        "--macro1_duration",
        metavar="Macro 1 Duration",
        help="Macro 1 Duration in Seconds",
        type=int,
        default=1,
        widget="IntegerField",
        gooey_options={"min": 1, "max": 99, "increment": 1},
    )
    macros.add_argument(
        "--macro2",
        metavar="Macro 2",
        help="Macro 2 Hotkey",
        choices=KEYS + [*SPECIAL_KEYS],
        type=str,
        widget="FilterableDropdown",
        gooey_options={"placeholder": "Optional"},
    )
    macros.add_argument(
        "--macro2_duration",
        metavar="Macro 2 Duration",
        help="Macro 2 Duration in Seconds",
        type=int,
        default=0,
        widget="IntegerField",
        gooey_options={"placeholder": "Optional", "min": 0, "max": 99, "increment": 1},
    )

    # Consumables
    consumables = parser.add_argument_group("Consumables")
    consumables.add_argument(
        "--food",
        metavar="Food",
        help="Food Hotkey",
        choices=KEYS + [*SPECIAL_KEYS],
        type=str,
        widget="FilterableDropdown",
        gooey_options={"placeholder": "Optional"},
    )
    consumables.add_argument(
        "--food_duration",
        metavar="Food Duration",
        choices=["30", "40", "45"],
        help="Duration of Food in Minutes",
    )
    consumables.add_argument(
        "--potion",
        metavar="Potion",
        help="Potion Hotkey",
        choices=KEYS + [*SPECIAL_KEYS],
        type=str,
        widget="FilterableDropdown",
        gooey_options={"placeholder": "Optional"},
    )

    # Settings
    settings = parser.add_argument_group("Settings")
    settings.add_argument(
        "confirm",
        metavar="Confirm",
        help="Confirm Hotkey",
        choices=KEYS + [*SPECIAL_KEYS],
        type=str,
        widget="FilterableDropdown",
        gooey_options={"placeholder": "Enter Key"},
    )
    settings.add_argument(
        "cancel",
        metavar="Cancel",
        help="Cancel Hotkey",
        choices=KEYS + [*SPECIAL_KEYS],
        type=str,
        widget="FilterableDropdown",
        gooey_options={"placeholder": "Enter Key"},
    )

    args = parser.parse_args()

    global debug
    debug = False
    if args.verbose:
        debug = True

    if debug:
        print("VERBOSE MODE")
        print("\n=====\n")
        print("ARGUMENTS:\n")
        print(f"START/PAUSE KEY: {args.start_pause}")
        print(f"STOP KEY: {args.stop}")
        print(f"MAX AMOUNT: {args.max_amount}")
        print(f"MACRO1 KEY: {args.macro1}")
        print(f"MACRO1 DURATION: {args.macro1_duration}")
        if args.macro2:
            print(f"MACRO2 KEY: {args.macro2}")
            print(f"MACRO2 DURATION: {args.macro2_duration}")
        if args.food:
            print(f"FOOD KEY: {args.food}")
            print(f"FOOD DURATION: {args.food_duration}")
        if args.potion:
            print(f"POTION KEY: {args.potion}")
        print(f"CONFIRM KEY: {args.confirm}")
        print(f"CANCEL KEY: {args.cancel}")

        print("\n=====\n")

    global start_pause_key
    start_pause_key = str_to_key(args.start_pause)

    if debug:
        try:
            print(f"START_PAUSE_KEY: {start_pause_key.char}")
        except AttributeError:
            print(f"START_PAUSE_KEY: {start_pause_key}")

    global stop_key
    stop_key = str_to_key(args.stop)

    if debug:
        try:
            print(f"STOP_KEY: {stop_key.char}")
        except AttributeError:
            print(f"STOP_KEY: {stop_key}")

    macro1_key = str_to_key(args.macro1)

    if debug:
        try:
            print(f"MACRO1_KEY: {macro1_key.char}")
        except AttributeError:
            print(f"MACRO1_KEY: {macro1_key}")

    if args.macro2:
        macro2_key = str_to_key(args.macro2)

        if debug:
            try:
                print(f"MACRO2_KEY: {macro2_key.char}")
            except AttributeError:
                print(f"MACRO2_KEY: {macro2_key}")
    else:
        macro2_key = None

    if args.food:
        food_key = str_to_key(args.food)

        if debug:
            try:
                print(f"FOOD_KEY: {food_key.char}")
            except AttributeError:
                print(f"FOOD_KEY: {food_key}")
    else:
        food_key = None

    if args.food_duration:
        food_duration = int(args.food_duration) * 60

        if debug:
            print(f"FOOD_DURATION: {food_duration}")
    else:
        food_duration = None

    if args.potion:
        potion_key = str_to_key(args.potion)

        if debug:
            try:
                print(f"POTION_KEY: {potion_key.char}")
            except AttributeError:
                print(f"POTION_KEY: {potion_key}")
    else:
        potion_key = None

    confirm_key = str_to_key(args.confirm)

    if debug:
        try:
            print(f"CONFIRM_KEY: {confirm_key.char}")
        except AttributeError:
            print(f"CONFIRM_KEY: {confirm_key}")

    cancel_key = str_to_key(args.cancel)

    if debug:
        try:
            print(f"CANCEL_KEY: {cancel_key.char}")
        except AttributeError:
            print(f"CANCEL_KEY: {cancel_key}")

    if debug:
        print("\n=====\n")

    global autocrafter_thread
    autocrafter_thread = XIVAutoCrafter(
        args.max_amount,
        macro1_key,
        args.macro1_duration,
        confirm_key,
        cancel_key,
        start_pause_key,
        stop_key,
        food_key,
        food_duration,
        potion_key,
        macro2_key,
        args.macro2_duration,
        debug,
    )
    autocrafter_thread.start()

    global keyboard
    keyboard = Controller()

    global listener
    with Listener(on_press=on_press) as listener:
        listener.join()


def on_press(key):
    if key == start_pause_key:
        if autocrafter_thread.running:
            autocrafter_thread.stop_autocrafter()
        else:
            autocrafter_thread.start_autocrafter()

    elif key == stop_key:
        autocrafter_thread.exit()
        listener.stop()


if __name__ == "__main__":
    main()
