from POM import PostsGrid_POM as grid
from POM import Screen_POM as screen
from POM import Locators as loc
import AnyBotLog as logg


class HashTagPage(screen.Screen):
    def __init__(self, driver):
        super().__init__(driver)
        self.tag = None
        self.grid = grid.PostGrid(self.driver)
        self.getOwnTitle()

    def getOwnTitle(self):
        tagObj = self.findElementBy_ID(loc.hashTagPage_ID['hashTag'])
        if tagObj:
            self.tag = tagObj.text

    def verifyPageType(self, tag='#'):
        self.getOwnTitle()
        if self.tag:
            logg.logSmth(f'##### Hastag title {self.tag}, verified', 'INFO')

            if '#' in self.tag:
                return True

        logg.logSmth('##### Hastag title not found! Are you in a hastag page for sure?', 'WARNING')
        return False

    def goToRecentPosts(self):
        recents = self.findElementBy_XPATH(self.loc.hashTagPage_Xpath['recent'])
        if recents:
            recents.click()
            self.reactionWait()

    def getPostCount(self):
        pass

    def likeHastagPostByOrder(self, order):
        self.grid.likePostByOrder(order)
