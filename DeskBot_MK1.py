from POM import Desktop_WebPage as wp

from Services import hashTagCount_DesktopService as htcdsktp


class DesktopBot:
    def __init__(self):
        self.getBrowser()

    def getBrowser(self):
        self.webPage = wp.WebPage(False)

    def hashCount_DesktopService(self):
        return htcdsktp.getTagsCount(self)
