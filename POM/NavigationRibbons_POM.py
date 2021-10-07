from POM import HomePage_POM as home
from POM import Locators as loc
from POM import Screen_POM as screen
from POM import SearchPage_POM as searchPage
from POM import UserPage_POM as up

import AnyBotLog as logg


class NavigationRibbons(screen.Screen):

    def goHome(self):
        bottomHomeButton = self.findElementBy_XPATH(loc.ribbon_XPath['bottomBar_homeButton'])

        if bottomHomeButton:
            self.doubleClick(bottomHomeButton)
            self.reactionWait()

            return home.HomePage(self.driver)

    def goToSearchPage(self):
        searchButton = self.findElementBy_XPATH(loc.ribbon_XPath['bottomBar_Search'])
        if searchButton:
            self.doubleClick(searchButton)
            self.reactionWait(5)

            return searchPage.SearchPage(self.driver)

    def goToOwnProfile(self):
        ownProfileButton = self.findElementBy_ID(loc.ribbon_ID['bottomBar_OwnProfile'])
        if ownProfileButton:
            self.doubleClick(ownProfileButton)
            self.reactionWait(1)

            return up.UserPage(self.driver)

    def goToOwnActivity(self):
        ownActivityButton = self.findElementBy_XPATH(loc.ribbon_XPath['activity'])
        if ownActivityButton:
            ownActivityButton.click()
            self.reactionWait(1)

    def goBack(self):
        backButton = self.findElementBy_ID(loc.ribbon_ID['backButton'])
        if backButton:
            backButton.click()
            # logg.logSmth(f"# Back button clicked?")
            self.reactionWait()
