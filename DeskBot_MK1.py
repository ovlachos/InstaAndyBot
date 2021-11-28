from POM import Desktop_WebPage as wp
from Services import hashTagCount_DesktopService as htcdsktp
from BotMemory import FileHandlerBot as fh


class DesktopBot:
    def __init__(self):
        self.getBrowser()
        self.fileHandler = fh.FileHandlerBot()

        self.targetHashtags_frame = self.fileHandler.CSV_getFrameFromCSVfile('hashtagsToLookForCSV')
        self.targetHashtags_List = self.targetHashtags_frame[self.targetHashtags_frame.columns[0]].tolist()

    def getBrowser(self):
        self.webPage = wp.WebPage(False)

    def hashCount_DesktopService(self):
        return htcdsktp.getTagsCount(self)
