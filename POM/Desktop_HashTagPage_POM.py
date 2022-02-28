# All POMs require a webPage object to be instantiated/initialized.
# The webPage object provides the webdriver and a "what page am I currently browsing" method
from time import sleep

xpaths = {
    # "postCount": "//div[@class='WSpok']//span[@class='g47SY ']",
    "postCount": "//span[@class='g47SY ']",
    "hashTag": "//div[@class='WSpok']//h1[@class='_7UhW9       fKFbl yUEEX   KV-D4          uL8Hv         ']",
    "posts": "//a[contains(@href,'/p/')]",
    # 'Most Recent' posts start after the top 9 posts //a[@author_id='1562742500'][@page_id='profilePage']
}


class HashTagPage:
    def __init__(self, webPage, hashtag):
        self.page = webPage
        self.driver = self.page.driver
        self.hashtag = hashtag

    def verifyHashtagHeading(self):
        heading = self.page.getPageElement_tryHard(xpaths['hashTag'])
        if heading:
            heading = heading.text

            if self.hashtag in heading:
                return True

        return False

    def getPostCount(self):
        try:
            return self.page.getPageElement_tryHard(xpaths['postCount']).text.replace(',', '')
        except Exception as e:
            print(e)
            return None
