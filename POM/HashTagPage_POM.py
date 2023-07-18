import AnyBotLog as logg
from POM import Locators as loc
from POM import PostsGrid_POM as grid
from POM import Screen_POM as screen


class HashTagPage(screen.Screen):
    def __init__(self, driver):
        super().__init__(driver)
        self.tag = None
        self.grid = grid.PostGrid(self.driver)
        self.getOwnTitle()

    def getOwnTitle(self):
        if tagObj := self.findElementBy_ID(loc.hashTagPage_ID['hashTag']):
            self.tag = tagObj.text

    def verifyPageType(self, tag='#'):
        self.getOwnTitle()
        if self.tag and '#' in self.tag:
            return True

        logg.logSmth('##### Hastag title not found! Are you in a hastag page for sure?', 'WARNING')
        return False

    def goToRecentPosts(self):
        if filterButton := self.findElementBy_XPATH(
            self.loc.hashTagPage_Xpath['recent']
        ):
            filterButton.click()
            self.reactionWait(3)

        if recents := self.findElementBy_XPATH(
            self.loc.hashTagPage_Xpath['recent']
        ):
            recents.click()
            self.reactionWait()

    def getPostCount(self):
        pass

    def likeHastagPostByOrder(self, order):
        self.grid.likePostByOrder(order)
