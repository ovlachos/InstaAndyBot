import auth
import unittest
import AndyBot_MK1 as bot
import AnyBotLog as logg
from appium import webdriver as wb
from Services import myStats_Service as mst


class test(unittest.TestCase):
    def setUp(self):
        desired_caps = {}
        desired_caps['deviceName'] = auth.getDeviceName()
        desired_caps['platformName'] = "Android"
        desired_caps['appPackage'] = "com.instagram.android"
        desired_caps['appActivity'] = "com.instagram.mainactivity.MainActivity"
        desired_caps['noReset'] = 'true'

        self.driver = wb.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.driver.implicitly_wait(5)
        self.driver.unlock()

        logg.logSmth(f"#" * 50)
        logg.logSmth(f"Device is {desired_caps['deviceName']}")

    def tearDown(self):
        self.driver.quit()

    def testRun(self):
        from time import sleep
        myBot = bot.AndyBot(self.driver, auth.getDevice())

        sleep(10)
        # myBot.set_wake_time()
        # myBot.sleep_computer()

        for i in range(2):
            myBot.botSleep(verbose=True)
            myBot.driver.unlock()

        try:
            # myBot.memoryManager.readStoredMemoryFile()
            myBot.myFollowers_Service(.50)
            # mode 1 start

        except Exception as e:
            logg.logSmth("\n" + "#" * 20 + "\n")
            logg.logSmth("Exception occurred @#$", 'ERROR')
            logg.logSmth("\n" + "#" * 20 + "\n")
        finally:
            logg.logSmth("\nEND OF TEST\n")

        t = 0

    def gameSortOf(self, unfollowList, bot):
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
                userNotFound_counter = 0  # restart this counter as we only want to see if we fail to get X users in a row, before shuting things down

                if 'OK' in userPage.unfollow():
                    # user.markDateUnfollowed()
                    # bot.memoryManager.updateUserRecord(user)

                    unfollow_counter += 1
                    logg.logSmth(f"##### {unfollow_counter} / {len(unfollowList)} users unfollowed today")

                    bot.botSleep()
        else:
            logg.logSmth(f"##### - {0} users to be un-Followed")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test)
    unittest.TextTestRunner(verbosity=1).run(suite)
