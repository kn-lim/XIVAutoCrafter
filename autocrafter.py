import time
import threading
from pynput.keyboard import Key, KeyCode, Controller, Listener

# Variables
DEBUG = True
CRAFTING_DELAY = 1
USE_FOOD = True
USE_POTION = True
FOOD_DURATION = 1  # minutes * 60
POTION_DURATION = 1  # minutes * 60
MACRO_1_DURATION = 1  # number of lines * 3
MACRO_2_DURATION = 1  # number of lines * 3
MAX_AMOUNT = 1

# Hotkeys
CONFIRM = KeyCode()
CANCEL = KeyCode()
FOOD = KeyCode()
POTION = KeyCode()
MACRO_1 = KeyCode()
MACRO_2 = KeyCode()

start_stop_key = KeyCode(char="a")
stop_key = KeyCode(char="b")


class AutoCrafter(threading.Thread):
    def __init__(self, delay, max_amount):
        super().__init__()
        self.delay = delay
        self.running = False
        self.program_running = True
        self.start_food_time = None
        self.start_potion_time = None
        self.counter = 0
        self.max_amount = max_amount

    def start_autocrafter(self):
        print("STARTING AUTOCRAFTER")
        self.running = True

    def stop_autocrafter(self):
        print("STOPPING AUTOCRAFTER")
        self.running = False

    @staticmethod
    def start_craft():
        keyboard.tap(CONFIRM)
        time.sleep(0.5)
        keyboard.tap(CONFIRM)
        time.sleep(0.5)
        keyboard.tap(CONFIRM)
        time.sleep(0.5)
        keyboard.tap(CONFIRM)
        time.sleep(3)

    @staticmethod
    def cancel_craft():
        keyboard.tap(CONFIRM)
        time.sleep(0.5)
        keyboard.tap(CANCEL)
        time.sleep(0.5)
        keyboard.tap(CONFIRM)
        time.sleep(3)

    def check_food(self):
        if DEBUG:
            print("CHECKING FOOD")

        if self.start_food_time is not None:
            difference = int(time.time()) - self.start_food_time

            if DEBUG:
                print(f"DIFFERENCE: {difference}")
                print(f"START FOOD TIME: {self.start_food_time}")

            if difference > FOOD_DURATION:
                self.consume_food()
            time.sleep(1)
        else:
            self.consume_food()

    def consume_food(self):
        print("CONSUMING FOOD")
        self.cancel_craft()
        self.start_food_time = int(time.time())
        keyboard.tap(FOOD)
        time.sleep(2)
        self.start_craft()

    def check_potion(self):
        if DEBUG:
            print("CHECKING POTION")

        if self.start_potion_time is not None:
            difference = int(time.time()) - self.start_potion_time

            if DEBUG:
                print(f"DIFFERENCE: {difference}")
                print(f"START POTION TIME: {self.start_potion_time}")

            if difference > POTION_DURATION:
                self.consume_potion()
            time.sleep(1)
        else:
            self.consume_potion()

    def consume_potion(self):
        print("CONSUMING POTION")
        self.cancel_craft()
        self.start_potion_time = int(time.time())
        keyboard.tap(POTION)
        time.sleep(2)
        self.start_craft()

    def exit(self):
        self.stop_autocrafter()
        self.program_running = False

    def run(self):
        while self.program_running:
            while self.running:
                self.start_craft()

                if USE_FOOD:
                    self.check_food()
                if USE_POTION:
                    self.check_potion()

                keyboard.tap(MACRO_1)
                time.sleep(MACRO_1_DURATION)

                if MACRO_2_DURATION != 0:
                    keyboard.tap(MACRO_2)
                    time.sleep(MACRO_2_DURATION)

                self.counter += 1
                if self.max_amount is not None:
                    print(f"CRAFTED: {self.counter} / {self.max_amount}")

                    if self.counter >= self.max_amount:
                        print("EXITING")
                        self.exit()
                else:
                    print(f"CRAFTED: {self.counter}")

                time.sleep(self.delay)
            time.sleep(1)


keyboard = Controller()
crafter_thread = AutoCrafter(CRAFTING_DELAY, MAX_AMOUNT)
crafter_thread.start()


def on_press(key):
    if DEBUG:
        try:
            print(f"alphanumeric key {key.char} pressed")

        except AttributeError:
            print(f"special key {key} pressed")

    if key == start_stop_key:
        if crafter_thread.running:
            crafter_thread.stop_autocrafter()
        else:
            crafter_thread.start_autocrafter()

    elif key == stop_key:
        crafter_thread.exit()
        listener.stop()


with Listener(on_press=on_press) as listener:
    listener.join()
