import auth
import sys
import unittest
import AndyBot_MK1 as bot
import AnyBotLog as logg

from appium import webdriver as wb
from Services import myStats_Service as mst


class test(unittest.TestCase):
    def setUp(self):

        desired_caps = {
            'deviceName': auth.getDeviceName(),
            'platformName': "Android",
            'appPackage': "com.instagram.android",
            'appActivity': "com.instagram.mainactivity.MainActivity",
            'noReset': 'true',
        }
        self.driver = wb.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.driver.implicitly_wait(5)
        self.driver.unlock()

        logg.logSmth("#" * 50)
        logg.logSmth(f"Device is {desired_caps['deviceName']}")

        self.bot = bot.AndyBot(self.driver, auth.getDevice())
        for _ in range(2):
            self.bot.botSleep(factor=0.02, verbose=True)
            self.bot.driver.unlock()

        # self.theHome()

    def tearDown(self):
        # self.driver.close_app()
        self.driver.terminate_app("com.instagram.android")
        self.driver.quit()
        if len(sys.argv) > 1:
            nameIs = str(sys.argv[1])
            logg.logSmth(f"\n\n{nameIs}\n\n")
        logg.logSmth("\n\nEND OF TEST\n\n")

    def testRun(self):
        funcDict = {
            "theListLike": self.theListLike,
            "theList": self.theList,
            "theGame": self.theGame,
            "theFollowingRecord": self.theFollowingRecord,
            "theFollowingCleanup": self.theFollowingCleanup,
            "theHome": self.theHome
        }

        memoryWritting = {
            "theListLike": False,  # working
            "theList": True,  # not working
            "theGame": True,
            "theFollowingRecord": False,
            "theFollowingCleanup": True,
            "theHome": False
        }

        nameIs = str(sys.argv[1]) if len(sys.argv) > 1 else "theListLike"
        print("The test to run is ", nameIs)
        func = funcDict.get(nameIs)
        memoryW = memoryWritting.get(nameIs)

        try:
            func()
        except Exception:
            logg.logSmth("#" * 20)
            logg.logSmth(f"Exception occurred @#$  {nameIs}", 'ERROR')
            logg.logSmth("#" * 20)
        finally:
            # logg.logSmth("#" * 20)
            # logg.logSmth(f"Exception occurred @#$  {nameIs}", 'ERROR')
            # logg.logSmth("#" * 20)
            logg.logSmth("#" * 20)
            logg.logSmth(
                f"########## Follow mana left: {self.bot.followMana} || {self.bot.followManaMax - self.bot.followMana} users followed today")
            logg.logSmth("#" * 20)
            if memoryW:
                logg.logSmth('write Memory to file before quiting')
                self.bot.memoryManager.writeMemoryFileToDrive()

    def theListLike(self):
        self.bot.theList_Service(numberOfTags=15, numberOfPostsPerTag=90, randomArgs=False, toLike=True, toFollow=False)

    def theList(self):
        self.bot.theList_Service(numberOfTags=18, numberOfPostsPerTag=4, randomArgs=False)

    def theHome(self):
        self.bot.myStats_Service()
        self.bot.homePageScroller(numberOfPosts=120, randomArgs=False)

    def theGame(self):
        # self.bot.myStats_Service()
        self.bot.theGame_Service(numberOfusersToCheck=30, randomArgs=False)

    def theFollowingRecord(self):
        self.bot.memoryManager.readStoredMemoryFile()
        mst.getMyFollowingList(self.bot)  # mode 1

        self.bot.sleep_computer()

    def theFollowingCleanup(self):
        self.bot.memoryManager.readStoredMemoryFile()

        mfollowingFrame = self.bot.fileHandler.CSV_getFrameFromCSVfile('myFollowing')
        mfollowing_ = mfollowingFrame.values.tolist()
        mfollowing = [item for sublist in mfollowing_ for item in sublist]

        mem = self.bot.memoryManager.listOfUserMemory

        one = [x for x in mem if x.dateUnFollowed_byMe]
        firstDraft_peopleAlreadyUnfollowed = [x for x in one if x.daysSinceYouGotFollowed_Unfollowed('unfollow') > 3]
        secondDraft_peopleAlreadyUnfollowed = [x for x in firstDraft_peopleAlreadyUnfollowed if
                                               x.daysSinceYouGotFollowed_Unfollowed('unfollow') < 190]
        for user in secondDraft_peopleAlreadyUnfollowed:
            if user.handle in mfollowing:
                print(
                    f'Still following user {user.handle}, marked as unfollowed on: {user.dateUnFollowed_byMe} and followed on: {user.dateFollowed_byMe}', )

        nameMemory_peopleAlreadyUnfollowed = list(secondDraft_peopleAlreadyUnfollowed)
        filteredList_shouldUnfollow = [x for x in nameMemory_peopleAlreadyUnfollowed if x.handle in mfollowing]

        print(len(filteredList_shouldUnfollow))
        self.gameSortOf(filteredList_shouldUnfollow, self.bot, mfollowing)

        self.bot.sleep_computer()

    def gameSortOf(self, unfollowList, bot, myFollowing):
        if unfollowList:
            logg.logSmth(f"##### - {len(unfollowList)} users to be un-Followed")

            userNotFound_counter = 0
            unfollow_counter = 0
            for user in unfollowList:
                # user.daysSinceYouGotFollowed_Unfollowed('follow', True)

                logg.logSmth(f"### Navigating to user {user.handle}")
                searchPage = None
                while not searchPage:
                    searchPage = bot.navRibons.goToSearchPage()
                    if not searchPage:
                        bot.navRibons.goBack()

                userPage = searchPage.navigateToUserPage(user.handle)

                if not userPage:
                    bot.memoryManager.userPageCannotBeFound(user)

                    userNotFound_counter += 1
                    if userNotFound_counter > 3:
                        return "No Internet - ...or search shadow ban"

                    continue

                logg.logSmth(f"########## Will unfollow user {user.handle}")
                userNotFound_counter = 0  # restart this counter as we only want to see if we fail to get X users in a row, before shutting things down

                if 'OK' in userPage.unfollow():
                    # user.markDateUnfollowed()
                    # bot.memoryManager.updateUserRecord(user)

                    unfollow_counter += 1
                    logg.logSmth(f"##### {unfollow_counter} / {len(unfollowList)} users unfollowed today")
                    myFollowing = [x for x in myFollowing if x != user.handle]
                    mst.BotStats.record_new_point(myFollowing, 'myFollowing')

                    bot.botSleep()
        else:
            logg.logSmth('##### - 0 users to be un-Followed')


def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(test)
    unittest.TextTestRunner(verbosity=1).run(suite)


if __name__ == '__main__':
    main()
