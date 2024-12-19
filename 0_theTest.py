import auth
import sys
import unittest
import AndyBot_MK1 as bot
import AnyBotLog as logg

from appium import webdriver as wb
from Services import myStats_Service as mst


class InstagramTestSuite(unittest.TestCase):
    APP_PACKAGE = "com.instagram.android"
    APP_ACTIVITY = "com.instagram.mainactivity.MainActivity"
    DRIVER_URL = 'http://localhost:4723/wd/hub'

    def setUp(self):
        self.driver = self._initialize_driver()
        self.bot = bot.AndyBot(self.driver, auth.getDevice())
        logg.logSmth("#" * 50)
        logg.logSmth(f"Device is {auth.getDeviceName()}")

        for _ in range(2):
            self.bot.botSleep(factor=0.02, verbose=True)
            self.bot.driver.unlock()

    def tearDown(self):
        self.driver.terminate_app(self.APP_PACKAGE)
        self.driver.quit()
        if len(sys.argv) > 1:
            logg.logSmth(f"\n\n{str(sys.argv[1])}\n\n")
        logg.logSmth("\n\nEND OF TEST\n\n")

    def _initialize_driver(self):
        """Initialize the WebDriver with desired capabilities."""
        desired_caps = self.get_desired_capabilities()
        driver = wb.Remote(self.DRIVER_URL, desired_caps)
        driver.implicitly_wait(5)
        driver.unlock()
        return driver

    def get_desired_capabilities(self):
        """Return desired capabilities required to launch the app."""
        return {
            'deviceName': auth.getDeviceName(),
            'platformName': "Android",
            'appPackage': self.APP_PACKAGE,
            'appActivity': self.APP_ACTIVITY,
            'noReset': 'true'
        }

    def testRun(self):
        function_mapping = {
            "theListLike": self.theListLike,
            "theList": self.theList,
            "theGame": self.theGame,
            "theFollowingRecord": self.theFollowingRecord,
            "theFollowingCleanup": self.theFollowingCleanup,
            "theHome": self.theHome
        }

        memory_writing = {
            "theListLike": False,
            "theList": True,
            "theGame": True,
            "theFollowingRecord": False,
            "theFollowingCleanup": True,
            "theHome": False
        }

        # nameIs controls the function to be run
        nameIs = str(sys.argv[1]) if len(sys.argv) > 1 else "theListLike"
        print("The test to run is", nameIs)

        func = function_mapping.get(nameIs)
        memory_write = memory_writing.get(nameIs, False)

        try:
            if func:
                func()
            else:
                logg.logSmth(f"Invalid test name: {nameIs}", "ERROR")
        except Exception as e:
            logg.logSmth("#" * 20)
            logg.logSmth(f"Exception occurred: {nameIs} -> {str(e)}", "ERROR")
            logg.logSmth("#" * 20)
        finally:
            logg.logSmth("#" * 20)
            logg.logSmth(
                f"########## Follow mana left: {self.bot.followMana} || {self.bot.followManaMax - self.bot.followMana} users followed today")
            logg.logSmth("#" * 20)
            if memory_write:
                logg.logSmth('Writing memory to file before quitting')
                self.bot.memoryManager.writeMemoryFileToDrive()

    def theListLike(self):
        self.bot.theList_Service(numberOfTags=15, numberOfPostsPerTag=90, randomArgs=False, toLike=True, toFollow=False)

    def theList(self):
        self.bot.theList_Service(numberOfTags=18, numberOfPostsPerTag=4, randomArgs=False)

    def theHome(self):
        self.bot.myStats_Service()
        self.bot.homePageScroller(numberOfPosts=120, randomArgs=False)

    def theGame(self):
        self.bot.theGame_Service(numberOfusersToCheck=30, randomArgs=False)

    def theFollowingRecord(self):
        self.bot.memoryManager.readStoredMemoryFile()
        mst.getMyFollowingList(self.bot)  # mode 1
        self.bot.sleep_computer()

    def theFollowingCleanup(self):
        self.bot.memoryManager.readStoredMemoryFile()
        following_frame = self.bot.fileHandler.CSV_getFrameFromCSVfile('myFollowing')
        current_following = [item for sublist in following_frame.values.tolist() for item in sublist]
        unfollow_candidates = [
            user for user in self.bot.memoryManager.listOfUserMemory
            if user.dateUnFollowed_byMe and 3 < user.daysSinceYouGotFollowed_Unfollowed('unfollow') < 190
        ]
        filtered_list = [u for u in unfollow_candidates if u.handle in current_following]
        print(len(filtered_list))
        self.gameSortOf(filtered_list, self.bot, current_following)
        self.bot.sleep_computer()

    def gameSortOf(self, unfollow_list, bot, my_following):
        logg.logSmth(f"##### - {len(unfollow_list)} users to be un-Followed")
        if unfollow_list:
            user_not_found_count = 0
            unfollow_count = 0
            for user in unfollow_list:
                logg.logSmth(f"### Navigating to user {user.handle}")
                search_page = bot.navRibons.goToSearchPage()
                while not search_page:
                    bot.navRibons.goBack()
                    search_page = bot.navRibons.goToSearchPage()
                user_page = search_page.navigateToUserPage(user.handle)
                if not user_page:
                    bot.memoryManager.userPageCannotBeFound(user)
                    user_not_found_count += 1
                    if user_not_found_count > 3:
                        return "No Internet - or search shadow ban"
                    continue
                logg.logSmth(f"########## Will unfollow user {user.handle}")
                user_not_found_count = 0  # Reset if successful
                if 'OK' in user_page.unfollow():
                    unfollow_count += 1
                    logg.logSmth(f"##### {unfollow_count} / {len} users unfollowed today")


def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(InstagramTestSuite)
    unittest.TextTestRunner(verbosity=1).run(suite)


if __name__ == '__main__':
    main()
