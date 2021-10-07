import auth
import unittest
import AndyBot_MK1 as bot
import AnyBotLog as logg
from appium import webdriver as wb


class test(unittest.TestCase):
    def setUp(self):
        desired_caps = {}
        desired_caps['deviceName'] = auth.getDeviceName()
        desired_caps['platformName'] = "Android"
        desired_caps['appPackage'] = "com.instagram.android"
        desired_caps['appActivity'] = "com.instagram.mainactivity.MainActivity"
        desired_caps['noReset'] = 'true'

        self.driver = wb.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.driver.implicitly_wait(3)
        self.driver.unlock()

        logg.logSmth(f"#" * 50)
        logg.logSmth(f"Device is {desired_caps['deviceName']}")

    def tearDown(self):
        self.driver.quit()

    def testRun(self):
        myBot = bot.AndyBot(self.driver, auth.getDevice())

        for i in range(2):
            myBot.botSleep(verbose=True)
            myBot.driver.unlock()

        try:
            homePage = myBot.navRibons.goHome()
            homePage.scrollArea.fastScreenScan()
            if len(homePage.scrollArea.posts):
                post = homePage.scrollArea.posts[0]
                bounds = post.pic.rect
                print(bounds)
                t = 0

            self.driver.close_app()
        except:
            logg.logSmth("\n" + "#" * 20 + "\n")
            logg.logSmth("Exception occurred @#$", 'ERROR')
            logg.logSmth("\n" + "#" * 20 + "\n")
        finally:
            logg.logSmth('write Memory to file before quiting')
            self.driver.lock()
            logg.logSmth("\nEND OF TEST\n")

        t = 0


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test)
    unittest.TextTestRunner(verbosity=1).run(suite)
