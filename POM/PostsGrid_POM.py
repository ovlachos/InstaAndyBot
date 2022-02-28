import AnyBotLog as logg

from POM import Locators as loc
from POM import Post_ScrolableArea_POM as postScrol
from POM import Screen_POM as screen


class PostGrid(screen.Screen):
    def __init__(self, driver, maxRows=4):
        super().__init__(driver)
        self.rowLimit = maxRows
        self.scrollablePostArea = None

    def openPostByOrder(self, order):
        if order < 1:
            order = 1
        row, col = self.translateOrderToGridCoordinates(order)
        self.openPostByGridCoordinates(row, col)

    def translateOrderToGridCoordinates(self, order):
        row = int(order / 3)
        column = order - row * 3
        if column > 0:
            row += 1
        else:
            column = 3

        return row, column

    def openPostByGridCoordinates(self, row, column):
        # No more than 4 rows are usually displayed
        if row > self.rowLimit:
            row = self.rowLimit
        if column > 3:
            column = 3

        postXPATH = loc.page_XPATH['postsGrid']
        postXPATH = postXPATH.replace("Row 1", f"Row {row}").replace("Column 1", f"Column {column}")

        post = self.findElementBy_XPATH(postXPATH)

        if not post:
            postXPATH = loc.page_XPATH['postsGrid']
            postXPATH = postXPATH.replace("Row 1", f"row {row}").replace("Column 1", f"column {column}")

            post = self.findElementBy_XPATH(postXPATH)

        if post:
            post.click()
            self.reactionWait(1.5)
            self.scrollablePostArea = postScrol.Post_ScrolableArea(self.driver)

    def likePostByOrder(self, order):  # starting from '1'
        self.openPostByOrder(order)
        for post in self.scrollablePostArea.posts:
            likeResponse = post.likePost()
            logg.logSmth(f"Like response for {post.postingUser} is {likeResponse}", 'INFO')
