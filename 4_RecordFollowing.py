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
            myBot.memoryManager.readStoredMemoryFile()

            # mode 1 start
            mst.getMyFollowingList(myBot)  # mode 1
            # mode 1 end

        except Exception as e:
            logg.logSmth("\n" + "#" * 20 + "\n")
            logg.logSmth("Exception occurred @#$", 'ERROR')
            logg.logSmth("\n" + "#" * 20 + "\n")
        finally:
            logg.logSmth("\nEND OF TEST\n")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test)
    unittest.TextTestRunner(verbosity=1).run(suite)
