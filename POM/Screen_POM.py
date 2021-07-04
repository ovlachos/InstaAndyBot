import random
import auth
from datetime import datetime
from functools import wraps
from time import sleep

from POM import Locators as loc
from appium.webdriver.common.touch_action import TouchAction

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


def reactionTime(length=1):
    return random.uniform(length * 2, length * 4)


def find_exception_handler(func):
    @wraps(func)
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"{func.__name__} failed")
            print(*args, **kwargs)
            print(f"The cause is: {e}")
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
        return self.driver.find_element_by_id(ID)

    @find_exception_handler
    def findElementsBy_ID(self, ID):
        return self.driver.find_elements_by_id(ID)

    @find_exception_handler
    def findElementBy_XPATH(self, XPATH):
        return self.driver.find_element_by_xpath(XPATH)

    @find_exception_handler
    def findElementsBy_XPATH(self, XPATH):
        return self.driver.find_elements_by_xpath()

    def fastType(self, passage, field):
        field.click()
        for ch in passage:
            field.send_keys(ch)

            sleep(random.uniform(0.080, 0.190))

    def slowType(self, passage, field):
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

    # TODO: clear up your swiping methods
    def getScrollLengthCoordinates(self, length='medium'):
        startX, endX, startY, endY, hold = 0, 0, 0, 0, 0

        if 'med' in length:
            startX = random.randint(750, 850)
            endX = random.randint(750, 850)
            startY = random.randint((self.screenBoundLower - 100), self.screenBoundLower)
            endY = random.randint(self.screenBoundUpper, (self.screenBoundUpper + 150))
            hold = random.randint(100, 400)

        if 'small' in length:
            startX = random.randint(750, 850)
            endX = random.randint(750, 850)
            startY = random.randint((self.screenBoundLower - 300), (self.screenBoundLower - 200))
            endY = random.randint(self.screenBoundUpper, (self.screenBoundUpper + 250))
            hold = random.randint(300, 600)

        return startX, endX, startY, endY, hold

    def vSwipe(self, length='medium'):
        # Coordinates randomised at start
        startX, endX, startY, endY, hold = self.getScrollLengthCoordinates(length)

        self.driver.swipe(startX, startY, endX, endY, hold)
        self.reactionWait(0.75)

    def touchA(self, height=300):
        height = height + 156
        h = (height) / 10
        while height > 0:
            print(f"Scrolled by {h}")
            height -= h
            print(f"Remaining height: {height}")

            actions = TouchAction(self.driver)
            actions.press(x=450, y=1900)
            actions.wait(500)
            actions.move_to(x=430, y=1899 - h)
            actions.release()
            actions.perform()

    def scroll_(self):
        self.driver.execute_script("mobile: scroll", {'direction': 'down'})

    def vScroll(self, length=0):
        percentage = 2.0
        height = 700
        constantsHeight = 513

        if length:
            percentage = 1 * (length + constantsHeight) / height

        paramsDictArea = {
            'left': 600, 'top': 700, 'width': 200, 'height': height,
            'direction': 'down',
            'speed': 1000,  # random.randint(400, 1000),
            'percent': percentage}

        paramsDictElementID = {
            'elementId': "TEST",
            'direction': 'down',
            'speed': 500,
            'percent': percentage}

        can_scroll_more = self.driver.execute_script('mobile: scrollGesture', paramsDictArea)
        print(can_scroll_more, f"Scrolled for {percentage * 100}% at a length of {length} while the height was {height}")

    def getIntoView(self, elem):
        self.driver.execute_script("arguments[0].scrollIntoView(true);", elem)

    def getPhotoBounds(self):
        try:
            photo = self.driver.find_element_by_id(loc.post_ID['pic'])
        except:
            photo = self.driver.find_element_by_id(loc.post_ID['imageCarousel'])

        photoHeight = photo.rect['height']
        print(f"Photo with ID {photo.id} has a height of {photoHeight}")
        return photoHeight

    def reactionWait(self, length=1, verbose=False):
        tminsecs = reactionTime(length)
        if verbose:
            print(f'sleep for {tminsecs}')
        sleep(tminsecs)

    def doubleClick(self, element):
        time_between_clicks = random.uniform(0.050, 0.140)
        element.click()
        sleep(time_between_clicks)
        element.click()
