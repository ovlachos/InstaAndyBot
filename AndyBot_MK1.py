import time
from datetime import datetime
from random import choice, randint

from BotMemory import BotParams as btprms
from BotMemory import FileHandlerBot as fh
from BotMemory import UserMemoryManager

from Services import theGame_Service as theGame
from Services import theList_Service as theList
from Services import homePageScroller_Service as homeScroller

from POM import NavigationRibbons_POM as ribon

timeStampFormat = "%m/%d/%Y, %H:%M:%S"


class AndyBot():
    def __init__(self, driver, deviceDict):
        self.driver = driver
        self.factor = 1
        self.ownFollowers = 1280

        self.fileHandler = fh.FileHandlerBot()
        self.memoryManager = UserMemoryManager.UserMemoryManager()
        self.botParams = btprms.BotParams()

        # Bot Params Default values (that get replaced later on, maybe)
        self.paramsTimeStamp = None
        self.timeUpperBound = 48
        self.timeLowerBound = 34
        self.timeLimitSinceLastLoved = 30
        self.followMana = 50
        self.followManaMax = 100

        ## Game vars Default values (that get replaced later on, maybe)
        self.daysBeforeIunFollow = 20 - 1
        self.daysBeforeIunLove = 5

        # List vars
        self.targetHashtags_frame = self.fileHandler.CSV_getFrameFromCSVfile('hashtagsToLookForCSV')
        self.targetHashtags_List = self.targetHashtags_frame[self.targetHashtags_frame.columns[0]].tolist()
        self.words_frame = self.fileHandler.CSV_getFrameFromCSVfile('wordsToLookForInBioCSV')
        self.words = self.words_frame[self.words_frame.columns[0]].tolist()

        self.loadParams()
        self.replenishFollowMana()

        self.getMainPage()

    def replenishFollowMana(self):
        timeStamp = datetime.now().strftime(timeStampFormat)
        if self.timeDiffForManaReplenishment() > 24:
            self.followMana = self.followManaMax
            self.botParams.updateMana(self.followManaMax, timeStamp)  # the only time a new timestamp is recorded on drive
        else:
            self.botParams.updateMana(self.followMana)

    def decrementFolowMana(self, delta):
        self.followMana = self.followMana - delta
        self.botParams.updateMana(self.followMana)

    def loadParams(self):
        params = self.botParams.getBotParams()
        if params:
            self.paramsTimeStamp = params['TimeStamp']
            self.timeUpperBound = params['sleepMaxSecs']
            self.timeLowerBound = params['sleepMinSecs']
            self.timeLimitSinceLastLoved = params['timeLimitSinceLastLoved']
            self.followMana = params['manaLeft']
            self.followManaMax = params['manaMax']

            self.daysBeforeIunFollow = params['daysBeforeIunFollow']
            self.daysBeforeIunLove = params['daysBeforeIunLove']

    def timeDiffForManaReplenishment(self):

        try:
            lastCheck_Time = datetime.strptime(self.paramsTimeStamp, timeStampFormat)
            now_DateTime = datetime.now()

            # Convert to Unix timestamp
            d1_ts = time.mktime(lastCheck_Time.timetuple())
            d2_ts = time.mktime(now_DateTime.timetuple())
            deltaT = int(d2_ts - d1_ts) / 60 / 60  # hours

            return deltaT
        except Exception as e:
            print(e)
            return 12

    def botSleep(self, factor=0.01, verbose=False):
        sleepTime = randint(self.timeLowerBound, self.timeUpperBound)
        sleepTime = int(factor * sleepTime)
        if verbose: print(f"Sleeping {sleepTime}")
        time.sleep(sleepTime)

    def delayOps(self, minimum=2, maximum=20):
        sleepTime = randint((minimum * 60), (maximum * 60))
        print(f'Sleeping for {int(sleepTime / 60)} minutes')
        time.sleep(sleepTime)

    def getMainPage(self):
        self.navRibons = ribon.NavigationRibbons(self.driver)

    def theGame_Service(self, numberOfusersToCheck=1, randomArgs=True):
        if randomArgs:
            numberOfusersToCheck = int(randint(1, 5) * self.factor)

        print(f" Number of users to check: {numberOfusersToCheck}")
        return theGame.playTheGame(self, numberOfusersToCheck)

    def theList_Service(self, numberOfTags=1, numberOfPostsPerTag=1, randomArgs=True):
        if randomArgs:
            numberOfTags = int(randint(1, 3) * self.factor)
            numberOfPostsPerTag = int(randint(1, 5) * self.factor)

        return theList.foilowOrCollectUsernamesFromHashtagPages(self, numberOfTags, numberOfPostsPerTag)

    def homePageScroller(self, numberOfPosts=30, randomArgs=True):
        if randomArgs:
            numberOfPosts = int(randint(10, 20) * self.factor)

        return homeScroller.homePageScroll(self, numberOfPosts)
