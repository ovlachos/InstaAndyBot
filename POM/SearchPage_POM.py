import random
from time import sleep

from fuzzywuzzy import process

import AnyBotLog as logg
from POM import HashTagPage_POM as hp
from POM import Locators as loc
from POM import Screen_POM as screen
from POM import UserPage_POM as up


class SearchPage(screen.Screen):

    def typeIntoSearchField(self, query, speed='slow'):
        if textBox := self.findElementBy_ID(loc.searchPage_ID['searchBarField']):
            if 'slow' in speed:
                self.slowType(query, textBox)
                self.driver.back()
            else:
                self.fastType(query, textBox)

    def getUserSearchResult(self):
        if resultsList := self.findElementsBy_ID(
                loc.searchPage_ID['resultsCommon_Users']
        ):
            return resultsList

    def getTagSearchResults(self):
        if resultsList := self.findElementsBy_ID(
                loc.searchPage_ID['resultsCommon_Tags']
        ):
            return resultsList

    def getFuzzyResults(self, userName):
        searchResults = self.getUserSearchResult()

        if searchResults and len(searchResults) > 0:
            userHandles = [item.text for item in searchResults]
            highest = process.extractOne(userName, userHandles)
            fuzzyMatch = highest[0]
            return fuzzyMatch, highest[1]

        return None, None

    def navigateToUserPage(self, username):
        divider = int(random.choice([0.4, 0.45, 0.55, 0.60]) * len(username))
        query_firstPart = username[:divider]
        query_secondPart = username[divider:]

        # Trying to get away with typing half the name
        results = self._extracted_from_navigateToUserPage_7(query_firstPart)
        # fuzzyMatch, score = self.getFuzzyResults(username)
        # if fuzzyMatch:
        #     if score > 90:

        if results:
            if element := [x for x in results if x.text == username]:
                element[0].click()
                # sleep(2)
                # logg.logSmth(f"### navigating to {fuzzyMatch} with an input of {username} and {query_firstPart}")
                return up.UserPage(self.driver)

        # If that did not work, then type the rest of it
        # logg.logSmth(f'### user not found | results are {[x.text for x in results]} and fuzzyMatch is {fuzzyMatch}')
        # logg.logSmth("### I need to type in more...")
        results = self._extracted_from_navigateToUserPage_7(query_secondPart)
        # fuzzyMatch, score = self.getFuzzyResults(username)
        # if fuzzyMatch:
        if results:
            if element := [x for x in results if x.text == username]:
                element[0].click()
                sleep(2)
                # logg.logSmth(f"### navigating to {fuzzyMatch} with an input of {username} and {query_firstPart}{query_secondPart}", "INFO")
                return up.UserPage(self.driver)

        # If no fuzzy match was found after both attempts then call it.
        if results:
            logg.logSmth(
                f'### user not found | results are {[x.text for x in results]} and fuzzyMatch is')  # {fuzzyMatch}')
        return None

    # TODO Rename this here and in `navigateToUserPage`
    def _extracted_from_navigateToUserPage_7(self, arg0):
        # Trying to get away with typing half the name
        self.typeIntoSearchField(arg0)
        self.reactionWait(0.5)
        return self.getUserSearchResult()

    def navigateToHashTagPage(self, tag):
        self.typeIntoSearchField(tag)
        self.reactionWait()
        if results := self.getTagSearchResults():
            results[0].click()
            self.reactionWait()
            return hp.HashTagPage(self.driver)

        return None
