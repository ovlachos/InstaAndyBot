import random
import AnyBotLog as logg

from time import sleep
from fuzzywuzzy import process

from POM import HashTagPage_POM as hp
from POM import Locators as loc
from POM import Screen_POM as screen
from POM import UserPage_POM as up


class SearchPage(screen.Screen):

    def typeIntoSearchField(self, query, speed='slow'):
        textBox = self.driver.find_element_by_id(loc.searchPage_ID['searchBarField'])
        if textBox:
            if 'slow' in speed:
                self.slowType(query, textBox)
                self.driver.back()
            else:
                self.fastType(query, textBox)

    def getUserSearchResult(self):
        resultsList = self.driver.find_elements_by_id(loc.searchPage_ID['resultsCommon_Users'])
        if resultsList:
            return resultsList

    def getTagSearchResults(self):
        resultsList = self.driver.find_elements_by_id(loc.searchPage_ID['resultsCommon_Tags'])
        if resultsList:
            return resultsList

    def getFuzzyResults(self, userName):
        searchResults = self.getUserSearchResult()

        userHandles = []
        if searchResults:
            if len(searchResults) > 0:
                for item in searchResults:
                    userHandles.append(item.text)

                highest = process.extractOne(userName, userHandles)
                fuzzyMatch = highest[0]
                return fuzzyMatch, highest[1]

        return None, None

    def navigateToUserPage(self, username):
        divider = int(random.choice([0.4, 0.45, 0.55, 0.60]) * len(username))
        query_firstPart = username[:divider]
        query_secondPart = username[divider:]

        # Trying to get away with typing half the name
        self.typeIntoSearchField(query_firstPart)

        self.reactionWait(0.5)

        results = self.getUserSearchResult()

        fuzzyMatch, score = self.getFuzzyResults(username)
        if fuzzyMatch:
            if score > 95:
                element = [x for x in results if x.text == fuzzyMatch]
                if element:
                    element[0].click()
                    sleep(2)
                    logg.logSmth(f"navigating to {fuzzyMatch} with an input of {username} and {query_firstPart}")
                    return up.UserPage(self.driver)

        else:
            logg.logSmth("I need to type in more...")
            # If that did not work, then type the rest of it
            self.typeIntoSearchField(query_secondPart)
            results = self.getUserSearchResult()

            fuzzyMatch, score = self.getFuzzyResults(username)
            if fuzzyMatch:
                element = [x for x in results if x.text == fuzzyMatch]
                if element:
                    element[0].click()
                    sleep(2)
                    logg.logSmth(f"navigating to {fuzzyMatch} with an input of {username} and {query_secondPart}", "INFO")
                    return up.UserPage(self.driver)

        logg.logSmth(f'user not found | results are {results} and fuzzyMatch is {fuzzyMatch}')
        return None

    def naviateToHashTagPage(self, tag):
        self.typeIntoSearchField(tag)
        results = self.getTagSearchResults()

        if results:
            results[0].click()
            self.reactionWait()
            return hp.HashTagPage(self.driver)

        return None
