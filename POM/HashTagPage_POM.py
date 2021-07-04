from POM import PostsGrid_POM as grid
from POM import Screen_POM as screen
from POM import Locators as loc


class HashTagPage(screen.Screen):
    def __init__(self, driver):
        super().__init__(driver)
        self.grid = grid.PostGrid(self.driver)
        self.getOwnTitle()

    def getOwnTitle(self):
        self.tag = self.findElementBy_ID(loc.hashTagPage_ID['hashTag'])

    def goToRecentPosts(self):
        recents = self.findElementBy_XPATH(self.loc.hashTagPage_Xpath['recent'])
        if recents:
            recents.click()
            self.reactionWait()

    def getPostCount(self):
        pass

    def likeHastagPostByOrder(self, order):
        self.grid.likePostByOrder(order)
