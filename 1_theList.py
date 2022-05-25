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
        self.driver.implicitly_wait(5)
        self.driver.unlock()

        logg.logSmth(f"#" * 50)
        logg.logSmth(f"Device is {desired_caps['deviceName']}")

    def tearDown(self):
        self.driver.quit()

    def testRun(self):
        myBot = bot.AndyBot(self.driver, auth.getDevice())

        for i in range(2):
            myBot.botSleep(factor=0.02, verbose=True)
            myBot.driver.unlock()

        try:
            myBot.theList_Service(numberOfTags=14, numberOfPostsPerTag=7, randomArgs=False)
            self.driver.close_app()
            self.driver.terminate_app("com.instagram.android")
        except:
            logg.logSmth("#" * 20 + "\n")
            logg.logSmth("Exception occurred @#$", 'ERROR')
            logg.logSmth("#" * 20 + "\n")
        finally:
            logg.logSmth('write Memory to file before quiting')
            myBot.memoryManager.writeMemoryFileToDrive()
            logg.logSmth("\n\nEND OF TEST\n")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test)
    unittest.TextTestRunner(verbosity=1).run(suite)
