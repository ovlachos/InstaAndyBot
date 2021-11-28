import random
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

from POM import Desktop_HashTagPage_POM as HSp

# All desktop POMs require a webPage object to be instantiated/initialized.
# The webPage object provides the webdriver

xpaths = {
    "GDPRcookies": "//button[contains(text(),'Accept')]",
}


class Browser:

    def __init__(self, headless=False):
        # ~~~ setting up a Firefox driver
        self.newSession = True

        self.createNewBrowserSession(headless)

    def createNewBrowserSession(self, headless):
        option = webdriver.ChromeOptions()
        option.add_argument('--disable-blink-features=AutomationControlled')
        option.add_argument("window-size=1280,800")
        option.add_argument("--start-maximized")

        option.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")

        self.driver = webdriver.Chrome(options=option)
        self.driver.implicitly_wait(5)

        executor_url = self.driver.command_executor._url
        session_id = self.driver.session_id

        print(f"New session with:\n\tsession_id: {session_id}\n\texecutor_url: {executor_url}\n")


class WebPage:

    def __init__(self, headless=False):
        self.instance = Browser(headless)
        self.driver = self.instance.driver

    def killBrowser(self):
        self.driver.quit()

    def tH_checkIfIhit_ActionLimit(self):
        try:
            errorMessagePresent = self.driver.find_element_by_xpath(
                "//p[contains(text(),'Please wait a few minutes')]").text
        except:
            return False

        if 'wait' in errorMessagePresent:
            return True

    def getPageElement_tryHard(self, xpath):
        attempts = 3
        result = None
        while result is None and attempts > 0:
            try:
                result = self.driver.find_element_by_xpath(xpath)
            except Exception as e:
                attempts -= 1

        return result

    def getPageElements_tryHard(self, xpath):
        attempts = 3
        result = None
        while result is None:
            try:
                result = self.driver.find_elements_by_xpath(xpath)
            except Exception as e:
                print(f"Could not get element {xpath}")
                attempts -= 1
                sleep(1)
                if attempts == 0:
                    break

        return result

    def safeClick(self, xpath):
        element = self.getPageElement_tryHard(xpath)
        if element:
            self.driver.execute_script("arguments[0].click();", element)
            sleep(3)
            return True
        return False

    def sendKey(self, key):
        if isinstance(key, str):
            try:
                actions = ActionChains(self.driver)
                actions.send_keys(key)
                actions.perform()
            except Exception as e:
                print(e)

    def sendESC(self):
        from selenium.webdriver.common.keys import Keys
        try:
            actions = ActionChains(self.driver)
            actions.send_keys(Keys.ESCAPE).perform()
            # self.driver.refresh()
        except Exception as e:
            print(f"ESC funciton: {e}")

    def slowTypeIntoField(self, fieldXPATH, query):
        try:

            field = self.getPageElement_tryHard(fieldXPATH)
            field.clear()
            for ch in query:
                sleep(random.uniform(0, 1))
                field.send_keys(ch)
            sleep(1)
        except Exception as e:
            print(e)

    def getListOfAtributeFromWebElementList(self, listOfWebElements, attribute):
        newList = []
        if listOfWebElements:
            for elem in listOfWebElements:
                newList.append(elem.get_attribute(attribute))

        return newList

    def getTitleAttributeFromWebElement(self, webElement):
        return webElement.get_attribute('title')

    def getTextFromWebElement(self, webElement):
        return webElement.text

    def sleepPage(self, secs):
        sleep(secs)

    def visitHashTagPage(self, tag):
        if '#' in tag:
            tag = tag.replace('#', '')

        self.driver.get(f"https://www.instagram.com/explore/tags/{tag}/")
        self.safeClick(xpaths['GDPRcookies'])
        return HSp.HashTagPage(self, tag)
