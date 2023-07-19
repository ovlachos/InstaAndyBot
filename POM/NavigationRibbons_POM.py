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
            return self._extracted_from_goToSearchPage_6(searchButton_by_ID)
        elif searchButton_by_Xpath:
            return self._extracted_from_goToSearchPage_6(searchButton_by_Xpath)

    # TODO Rename this here and in `goToSearchPage`
    def _extracted_from_goToSearchPage_6(self, arg0):
        self.doubleClick(arg0)
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
