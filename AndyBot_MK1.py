import os
import time
import AnyBotLog as logg
from datetime import datetime
from random import randint

from BotMemory import BotParams as btprms
from BotMemory import FileHandlerBot as fh
from BotMemory import UserMemoryManager

from Services import theGame_Service as theGame
from Services import theList_Service as theList
from Services import homePageScroller_Service as homeScroller
from Services import myStats_Service as statService

from POM import NavigationRibbons_POM as ribon

timeStampFormat = "%m/%d/%Y-%H:%M"


# TODO How to guarantee that every step of the way, navigating on the app is successful and I am not stuck on a previous/next page

class AndyBot():
    def __init__(self, driver, deviceDict):
        self.driver = driver
        self.factor = 1

        self.fileHandler = fh.FileHandlerBot()
        self.memoryManager = UserMemoryManager.UserMemoryManager()
        self.botParams = btprms.BotParams()

        # Bot Params Default values (that get replaced later on, maybe)
        self.ownFollowers = 3500
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
        logg.logSmth(f"Follow Mana: {self.followMana}/{self.followManaMax}")

        self.getMainPage()

    def sleep_computer(self):
        os.system("osascript -e 'tell application \"Finder\" to sleep'")

    def set_wake_time(self):
        os.system('sudo pmset schedule sleep "09/22/22 20:45:00" ')

    def replenishFollowMana(self):
        timeStamp = datetime.now().strftime(timeStampFormat)
        if self.timeDiffForManaReplenishment() > 24:
            self.followMana = self.followManaMax
            self.botParams.updateMana(self.followManaMax, timeStamp)  # the only time a new timestamp is recorded on drive
        else:
            self.botParams.updateMana(self.followMana)

    def updateOwnFollowers(self, count):
        self.botParams.updateOwnFollowers(count)

    def decrementFolowMana(self, delta):
        self.followMana = self.followMana - delta
        self.botParams.updateMana(self.followMana)

    def loadParams(self):
        params = self.botParams.getBotParams()
        if params:
            self.ownFollowers = params['OwnFollowers']
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
            lastCheck_Time = self.getDateTimeFromString(self.paramsTimeStamp)
            now_DateTime = self.getDateTimeNow()

            return self.calcTimeDiff(lastCheck_Time, now_DateTime)
        except Exception as e:
            logg.logSmth(e)
            return 12

    def calcTimeDiff(self, t1, t2):
        # Convert to Unix timestamp
        d1_ts = time.mktime(t1.timetuple())
        d2_ts = time.mktime(t2.timetuple())
        deltaT = int(d2_ts - d1_ts) / 60 / 60  # hours
        return deltaT

    def getDateTimeNow(self):
        return datetime.now()

    def getTimeStampString(self):
        return datetime.now().strftime(timeStampFormat)

    def getDateTimeFromString(self, timestamp):
        return datetime.strptime(timestamp, timeStampFormat)

    def botSleep(self, factor=0.05, verbose=False):
        sleepTime = randint(self.timeLowerBound, self.timeUpperBound)
        sleepTime = int(factor * sleepTime)
        if verbose: logg.logSmth(f"Sleeping {sleepTime}")
        time.sleep(sleepTime)

    def delayOps(self, minimum=2, maximum=20):
        sleepTime = randint((minimum * 60), (maximum * 60))
        logg.logSmth(f'Sleeping for {int(sleepTime / 60)} minutes')
        time.sleep(sleepTime)

    def getMainPage(self):
        self.navRibons = ribon.NavigationRibbons(self.driver)

    def theGame_Service(self, numberOfusersToCheck=1, randomArgs=True):
        if randomArgs:
            numberOfusersToCheck = int(randint(1, 5) * self.factor)

        logg.logSmth(f" Number of users to check: {numberOfusersToCheck}")
        return theGame.playTheGame(self, numberOfusersToCheck)

    def theList_Service(self, numberOfTags=1, numberOfPostsPerTag=1, randomArgs=True, toLike=True, toFollow=True):
        if randomArgs:
            numberOfTags = int(randint(1, 3) * self.factor)
            numberOfPostsPerTag = int(randint(1, 5) * self.factor)

        return theList.followOrCollectUsernamesFromHashtagPages(self, numberOfTags, numberOfPostsPerTag, toLike, toFollow)

    def homePageScroller(self, numberOfPosts=30, randomArgs=True):
        if randomArgs:
            numberOfPosts = int(randint(10, 20) * self.factor)

        return homeScroller.homePageScroll(self, numberOfPosts)

    def myStats_Service(self):
        return statService.getMyStats(self)

    def myFollowing_Service(self, percentage=1):
        return statService.getMyFollowingList(self)

    def myFollowers_Service(self, percentage=1):
        return statService.getMyFollowerList(self, percentage)
