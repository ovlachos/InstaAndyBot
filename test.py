import auth
import unittest
import AndyBot_MK1 as bot
from appium import webdriver as wb


class test(unittest.TestCase):
    def setUp(self):
        desired_caps = {}
        desired_caps['deviceName'] = auth.getDeviceName()
        desired_caps['platformName'] = "Android"
        desired_caps['noReset'] = 'true'

        self.driver = wb.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.driver.implicitly_wait(5)
        self.driver.unlock()
        logg.logSmth(f"Device is {desired_caps['deviceName']}")

    def tearDown(self):
        self.driver.quit()

    def testRun(self):
        myBot = bot.AndyBot(self.driver, auth.getDevice())

        for i in range(2):
            myBot.botSleep(verbose=True)
            myBot.driver.unlock()

        jsonTh = myBot.memoryManager.getMemoryFile()
        myBot.memoryManager.pickleMemoryFileToDrive()
        myBot.memoryManager.readMemoryFileFromDriveJSON()

        pickleTh = myBot.memoryManager.getMemoryFile()

        comparision = [x for x in jsonTh if x not in pickleTh]

        t = 0


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test)
    unittest.TextTestRunner(verbosity=1).run(suite)
