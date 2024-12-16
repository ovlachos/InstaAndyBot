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
    """
    Represents a web page with a specific hashtag, facilitating verification of
    hashtag presence and retrieval of post count.

    This class models the interaction and data extraction capabilities for a 
    web page related to a particular hashtag. It allows the user to verify 
    the hashtag displayed on the page and fetch the associated post count. 
    It assumes the use of predefined xpaths for locating specific elements.

    :ivar page: Represents the web page instance.
    :type page: WebPage
    :ivar driver: The web driver in use for the page.
    :type driver: Any
    :ivar hashtag: The hashtag associated with the page.
    :type hashtag: str
    """
    def __init__(self, webPage, hashtag):
        self.page = webPage
        self.driver = self.page.driver
        self.hashtag = hashtag

    def verifyHashtagHeading(self):
        """
        Verifies if the hashtag heading is present on the page and matches the
        expected hashtag.

        Returns a boolean value indicating the presence and correctness of the
        hashtag heading in the page element.

        :return: True if the hashtag is present and matches the expected value,
            False otherwise.
        :rtype: bool
        """
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
