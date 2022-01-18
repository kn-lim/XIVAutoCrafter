import time
import threading
import argparse
from pynput.keyboard import Key, KeyCode, Controller, Listener
from gooey import Gooey

# Constants
VERSION = "v0.1.0"
COPYRIGHT = "2022"

POTION_DURATION = 900
SPECIAL_KEYS = {
    "insert": Key.insert,
    "delete": Key.delete,
    "home": Key.home,
    "end": Key.end,
    "page_up": Key.page_up,
    "page_down": Key.page_down,
}


class XIVAutoCrafter(threading.Thread):
    def __init__(
        self,
        delay,
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
        self.delay = delay
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
            print("PAUSING AUTOCRAFTER")

        self.running = False

    def exit(self):
        self.stop_autocrafter()

        if self.debug:
            print("EXITING AUTOCRAFTER")

        self.program_running = False

    def start_craft(self):
        keyboard.tap(self.confirm)
        time.sleep(0.3)
        keyboard.tap(self.confirm)
        time.sleep(0.3)
        keyboard.tap(self.confirm)
        time.sleep(2)

    def cancel_craft(self):
        keyboard.tap(self.confirm)
        time.sleep(0.3)
        keyboard.tap(self.cancel)
        time.sleep(0.3)
        keyboard.tap(self.confirm)
        time.sleep(2)

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
        time.sleep(3)

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
        time.sleep(2)

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

                time.sleep(self.delay)
            time.sleep(0.5)


def str_to_key(string):
    if len(string) == 1:
        key = KeyCode(char=string)

    else:
        key = SPECIAL_KEYS[string]

    return key

@Gooey(
    program_name="XIVAutoCrafter", 
    program_description="A FFXIV Automated Crafting Tool",
    image_dir="images",
    menu=[{
        "name": "File",
        "items": [{
            "type": "AboutDialog",
            "menuTitle": "About",
            "name": "XIVAutoCrafter",
            "description": "A FFXIV Automated Crafting Tool",
            "version": VERSION,
            "copyright": COPYRIGHT,
            "website": "https://github.com/kn-lim/XIVAutoCrafter",
            "license": "MIT"
        }]
    }],
    progress_regex=r"^CRAFTED: (\d+) / (\d+)",
    progress_expr="x[0] / x[1] * 100"
)
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="increase output verbosity"
    )
    parser.add_argument("-f", "--food", help="use food option and hotkey")
    parser.add_argument(
        "--food_duration",
        choices=["30", "40", "45"],
        help="duration of food in minutes",
    )
    parser.add_argument("-p", "--potion", help="use potion option and hotkey")
    parser.add_argument("delay", type=int, help="sets delay per craft")
    parser.add_argument("max_amount", type=int, help="maximum amount to craft")
    parser.add_argument("macro1", help="macro 1 hotkey")
    parser.add_argument("macro1_duration", type=int, help="macro 1 duration in seconds")
    parser.add_argument("-m2", "--macro2", help="macro 2 hotkey")
    parser.add_argument("--macro2_duration", type=int, help="macro 2 duration in seconds")
    parser.add_argument("confirm", help="confirm hotkey")
    parser.add_argument("cancel", help="cancel hotkey")
    parser.add_argument("start_pause", help="start/pause XIVAutoCrafter hotkey")
    parser.add_argument("stop", help="stop XIVAutoCrafter hotkey")

    args = parser.parse_args()

    if args.verbose:
        print("VERBOSE MODE")
        print("\n=====\n")
        print("ARGUMENTS:\n")
        if args.food:
            print(f"FOOD KEY: {args.food}")
        if args.food_duration:
            print(f"FOOD DURATION: {args.food_duration}")
        if args.potion:
            print(f"POTION KEY: {args.potion}")
        print(f"DELAY: {args.delay}")
        print(f"MAX AMOUNT: {args.max_amount}")
        print(f"MACRO1 KEY: {args.macro1}")
        print(f"MACRO1 DURATION: {args.macro1_duration}")
        if args.macro2:
            print(f"MACRO2 KEY: {args.macro2}")
        if args.macro2_duration:
            print(f"MACRO2 DURATION: {args.macro2_duration}")
        print(f"CONFIRM KEY: {args.confirm}")
        print(f"CANCEL KEY: {args.cancel}")
        print(f"START/STOP KEY: {args.start_pause}")
        print(f"STOP KEY: {args.stop}")
        print("\n=====\n")

    macro1_key = str_to_key(args.macro1)

    if args.verbose:
        try:
            print(f"MACRO1_KEY: {macro1_key.char}")
        except AttributeError:
            print(f"MACRO1_KEY: {macro1_key}")

    confirm_key = str_to_key(args.confirm)

    if args.verbose:
        try:
            print(f"CONFIRM_KEY: {confirm_key.char}")
        except AttributeError:
            print(f"CONFIRM_KEY: {confirm_key}")

    cancel_key = str_to_key(args.cancel)

    if args.verbose:
        try:
            print(f"CANCEL_KEY: {cancel_key.char}")
        except AttributeError:
            print(f"CANCEL_KEY: {cancel_key}")

    global start_pause_key
    start_pause_key = str_to_key(args.start_pause)

    if args.verbose:
        try:
            print(f"START_PAUSE_KEY: {start_pause_key.char}")
        except AttributeError:
            print(f"START_PAUSE_KEY: {start_pause_key}")

    global stop_key
    stop_key = str_to_key(args.stop)

    if args.verbose:
        try:
            print(f"STOP_KEY: {stop_key.char}")
        except AttributeError:
            print(f"STOP_KEY: {stop_key}")

    if args.food:
        food_key = str_to_key(args.food)

        if args.verbose:
            try:
                print(f"FOOD_KEY: {food_key.char}")
            except AttributeError:
                print(f"FOOD_KEY: {food_key}")
    else:
        food_key = None

    if args.food_duration:
        food_duration = int(args.food_duration) * 60

        if args.verbose:
            print(f"FOOD_DURATION: {food_duration}")
    else:
        food_duration = None

    if args.potion:
        potion_key = str_to_key(args.potion)

        if args.verbose:
            try:
                print(f"POTION_KEY: {potion_key.char}")
            except AttributeError:
                print(f"POTION_KEY: {potion_key}")
    else:
        potion_key = None

    if args.macro2:
        macro2_key = str_to_key(args.macro2)

        if args.verbose:
            try:
                print(f"MACRO2_KEY: {macro2_key.char}")
            except AttributeError:
                print(f"MACRO2_KEY: {macro2_key}")

            print("\n=====\n")
    else:
        macro2_key = None

    global autocrafter_thread
    autocrafter_thread = XIVAutoCrafter(
        args.delay,
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
        args.verbose,
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
