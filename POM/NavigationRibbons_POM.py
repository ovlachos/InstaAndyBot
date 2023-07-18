from POM import HomePage_POM as home
from POM import Locators as loc
from POM import Screen_POM as screen
from POM import SearchPage_POM as searchPage
from POM import UserPage_POM as up

import AnyBotLog as logg


class NavigationRibbons(screen.Screen):

    def goHome(self):
        if bottomHomeButton := self.findElementBy_XPATH(
            loc.ribbon_XPath['bottomBar_homeButton']
        ):
            self.doubleClick(bottomHomeButton)
            self.vSwipeDown()
            self.reactionWait()

            return home.HomePage(self.driver)

    def goToSearchPage(self):
        searchButton_by_ID = self.findElementBy_ID(loc.ribbon_ID['bottomBar_searchPage'])
        searchButton_by_Xpath = self.findElementBy_XPATH(loc.ribbon_XPath['bottomBar_Search'])

        if searchButton_by_ID:
            self.doubleClick(searchButton_by_ID)
            self.reactionWait(3)

            return searchPage.SearchPage(self.driver)

        elif searchButton_by_Xpath:
            self.doubleClick(searchButton_by_Xpath)
            self.reactionWait(3)

            return searchPage.SearchPage(self.driver)

    def goToOwnProfile(self):
        if ownProfileButton := self.findElementBy_ID(
            loc.ribbon_ID['bottomBar_OwnProfile']
        ):
            self.doubleClick(ownProfileButton)
            self.reactionWait(1)
            self.vSwipeDown()

            return up.UserPage(self.driver)

    def goToOwnActivity(self):
        if ownActivityButton := self.findElementBy_XPATH(
            loc.ribbon_XPath['activity']
        ):
            ownActivityButton.click()
            self.reactionWait(1)

    def goBack(self):
        if backButton := self.findElementBy_ID(loc.ribbon_ID['backButton']):
            backButton.click()
        else:
            self.driver.back()
        # logg.logSmth(f"# Back button clicked?")
        self.reactionWait()
