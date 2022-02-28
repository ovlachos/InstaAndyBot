import random

import auth
from selenium.webdriver.common.by import By
from appium.webdriver.common.touch_action import TouchAction
import AnyBotLog as logg

from functools import wraps
from time import sleep

from POM import Locators as loc

myDict = {
    '_': 69,  # same as '-' minus symbol but with shift metastate
    'KEYCODE_HOME': 3,
    # Back 'KEY. */,
    'KEYCODE_BACK': 4,
    # '0' 'KEY. */,
    '0': 7,
    # '1' 'KEY. */,
    '1': 8,
    # '2' 'KEY. */,
    '2': 9,
    # '3' 'KEY. */,
    '3': 10,
    # '4' 'KEY. */,
    '4': 11,
    # '5' 'KEY. */,
    '5': 12,
    # '6' 'KEY. */,
    '6': 13,
    # '7' 'KEY. */,
    '7': 14,
    # '8' 'KEY. */,
    '8': 15,
    # '9' 'KEY. */,
    '9': 16,
    # '*' 'KEY. */,
    '*': 17,
    # '#' 'KEY. */,
    '#': 18,
    # Clear 'KEY. */,
    'KEYCODE_CLEAR': 28,
    # 'A' 'KEY. */,
    'a': 29,
    # 'B' 'KEY. */,
    'b': 30,
    # 'C' 'KEY. */,
    'c': 31,
    # 'D' 'KEY. */,
    'd': 32,
    # 'E' 'KEY. */,
    'e': 33,
    # 'F' 'KEY. */,
    'f': 34,
    # 'G' 'KEY. */,
    'g': 35,
    # 'H' 'KEY. */,
    'h': 36,
    # 'I' 'KEY. */,
    'i': 37,
    # 'J' 'KEY. */,
    'j': 38,
    # 'K' 'KEY. */,
    'k': 39,
    # 'L' 'KEY. */,
    'l': 40,
    # 'M' 'KEY. */,
    'm': 41,
    # 'N' 'KEY. */,
    'n': 42,
    # 'O' 'KEY. */,
    'o': 43,
    # 'P' 'KEY. */,
    'p': 44,
    # 'Q' 'KEY. */,
    'q': 45,
    # 'R' 'KEY. */,
    'r': 46,
    # 'S' 'KEY. */,
    's': 47,
    # 'T' 'KEY. */,
    't': 48,
    # 'U' 'KEY. */,
    'u': 49,
    # 'V' 'KEY. */,
    'v': 50,
    # 'W' 'KEY. */,
    'w': 51,
    # 'X' 'KEY. */,
    'x': 52,
    # 'Y' 'KEY. */,
    'y': 53,
    # 'Z' 'KEY. */,
    'z': 54,
    # ',' 'KEY. */,
    ',': 55,
    # '.' 'KEY. */,
    '.': 56,
    # Left Shift modifier 'KEY. */,
    'KEYCODE_SHIFT_LEFT': 59,
    # Right Shift modifier 'KEY. */,
    'KEYCODE_SHIFT_RIGHT': 60,
    # Space 'KEY. */,
    ' ': 62,
    # Enter 'KEY. */,
    'KEYCODE_ENTER': 66,
    # Backspace 'KEY.,
    # *Deletes characters before the insertion point, unlike { @ link  # 'KEYCODE_FORWARD_DEL}. */,
    'KEYCODE_DEL': 67,
    # '`' (backtick) 'KEY. */,
    '`': 68,
    # '-'. */,
    '-': 69,
    # ':' 'KEY. */,
    '=': 70,
    # '[' 'KEY. */,
    '[': 71,
    # ']' 'KEY. */,
    ']': 72,
    # '\' 'KEY. */,
    "\\": 73,
    # '' 'KEY. */,
    ';': 74,
    # ''' (apostrophe) 'KEY. */,
    '\'': 75,
    # '/' 'KEY. */,
    '/': 76,
    # '@' 'KEY. */,
    '@': 77,
    # '+' 'KEY. */,
    '+': 81,
}


def reactionTime(scale=1):
    return random.uniform(scale * 3, scale * 5)


def find_exception_handler(func):
    @wraps(func)
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:

            if "DOM" not in e.args[0] and "@content-desc" not in args[1]:
                logg.logSmth(f"The cause is: {e}", 'WARNING')
                logg.logSmth(args[1], 'WARNING')

            return None

    return inner_function


class Screen():
    def __init__(self, driver):
        self.driver = driver
        self.loc = loc

        self.device = auth.getDevice()
        self.deviceName = self.device['name']
        self.screenBoundUpper = self.device['upperScreenBound']
        self.screenBoundLower = self.device['lowerScreenBound']

    @find_exception_handler
    def findElementBy_ID(self, ID):
        return self.driver.find_element(by=By.ID, value=ID)

    @find_exception_handler
    def findElementsBy_ID(self, ID):
        return self.driver.find_elements(by=By.ID, value=ID)

    @find_exception_handler
    def findElementBy_XPATH(self, XPATH):
        return self.driver.find_element(by=By.XPATH, value=XPATH)

    @find_exception_handler
    def findElementsBy_XPATH(self, XPATH):
        return self.driver.find_elements(by=By.XPATH, value=XPATH)

    def getAndClickElementBy_ID(self, elementLocator):
        button = self.findElementBy_ID(elementLocator)
        if button:
            button.click()
            self.reactionWait(.5)
            return True
        return False

    def getAndClickElementBy_XPATH(self, elementLocator):
        button = self.findElementBy_XPATH(elementLocator)
        if button:
            button.click()
            self.reactionWait(.5)
            return True
        return False

    def fastType(self, passage, field):
        field.click()
        for ch in passage:
            field.send_keys(ch)

            sleep(random.uniform(0.080, 0.190))

    def slowType(self, passage, field):
        field.click()
        self.reactionWait(.2)
        field.click()

        for ch in passage:
            keyCode = self.getKeycode(ch)
            if keyCode:
                if '_' in ch:
                    self.driver.press_keycode(keyCode, metastate=193)  # shift + '-'
                    continue

                self.driver.press_keycode(keyCode)
            else:
                field.send_keys(ch)

    def getKeycode(self, key):

        keycode = myDict.get(key, None)

        return keycode

    def getScrollLengthCoordinates(self, length='medium'):
        startX, endX, startY, endY, hold = 0, 0, 0, 0, 0

        if 'med' in length:
            startX = random.randint(700, 800)
            endX = random.randint(700, 800)
            startY = random.randint((self.screenBoundLower - 100), self.screenBoundLower)
            endY = random.randint(self.screenBoundUpper, (self.screenBoundUpper + 150))
            hold = random.randint(100, 400)

        if 'small' in length:
            startX = random.randint(700, 800)
            endX = random.randint(700, 800)
            # startY = random.randint((self.screenBoundLower - 300), (self.screenBoundLower - 200))
            # endY = random.randint(self.screenBoundUpper, (self.screenBoundUpper + 250))
            startY = random.randint(1300, 1550)
            endY = random.randint(700, 850)
            hold = random.randint(600, 660)
            # print(startY, endY)

        if 'tiny' in length:
            startX = random.randint(700, 800)
            endX = random.randint(700, 800)
            startY = random.randint(1300, 1500)
            endY = random.randint(800, 1000)
            hold = random.randint(666, 666)
            # print(startY, endY)

        return startX, endX, startY, endY, hold

    def vSwipeDown(self, length='medium'):
        # Coordinates randomised at start
        startX, endX, startY, endY, hold = self.getScrollLengthCoordinates(length)

        self.driver.swipe(startX, endY, endX, startY)
        self.reactionWait(0.75)

    def vSwipeUp(self, length='medium'):
        # Coordinates randomised at start
        startX, endX, startY, endY, hold = self.getScrollLengthCoordinates(length)

        self.driver.swipe(startX, startY, endX, endY)
        self.reactionWait(0.75)

    def getPhotoBounds(self):
        try:
            photo = self.findElementBy_ID(loc.post_ID['pic'])
        except:
            photo = self.findElementBy_ID(loc.post_ID['imageCarousel'])
        finally:
            if not photo:
                return 0, 0

        photoHeight = photo.rect['height']
        photoWidth = photo.rect['width']

        return photoHeight, photoWidth

    def reactionWait(self, scale=1, verbose=False):
        tminsecs = reactionTime(scale)
        if verbose:
            logg.logSmth(f'sleep for {tminsecs}', 'INFO')
        sleep(tminsecs)

    def doubleClick(self, element):
        time_between_clicks = random.uniform(0.050, 0.140)
        element.click()
        sleep(time_between_clicks)
        element.click()

    def doubleClickCoordinates(self, x, y):
        padding = 0.02
        if self.screenBoundUpper * (1 + padding) < y < (1 - padding) * self.screenBoundLower:  # add 2% padding on the screen edges
            time_between_clicks = random.randint(50, 110)

            for i in range(2):
                actions = TouchAction(self.driver)
                actions.tap(x=x, y=y)
                actions.wait(time_between_clicks)
                actions.perform()
