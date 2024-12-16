import auth
import sys
import unittest
import AndyBot_MK1 as bot
import AnyBotLog as logg

from appium import webdriver as wb
from Services import myStats_Service as mst


class test(unittest.TestCase):
    """
    Test suite for automated Instagram-related bot functionalities.

    Defines a series of tests to automate operations such as following/unfollowing
    users, liking posts, capturing user data, and more. Each test is designed to
    interact with specified APIs and modules like memory management, bot navigation,
    and data analytics. This suite assumes a pre-configured Android test environment
    and uses Appium for automating Android device operations.

    :ivar driver: Instance of the WebDriver used to manage mobile automation.
    :type driver: WebDriver
    :ivar bot: Instance of the AndyBot class to perform Instagram-related operations.
    :type bot: AndyBot
    """
    def setUp(self):
        """
        Sets up the desired capabilities and initializes the necessary components required
        for interacting with an Android application using Appium. It configures the device
        and driver, establishes the communication endpoint, and prepares the `AndyBot`
        instance for performing automated interactions.

        :raises Exception: If driver initialization or device interaction fails

        Attributes:
            desired_caps (dict): Dictionary containing configuration for desired
                capabilities such as `platformName`, `appPackage`, and `appActivity`.
            driver (webdriver): The Appium driver connected to the specified mobile
                device and application.
            bot (AndyBot): Instance of the AndyBot class initialized for automated
                interactions with the mobile application.
        """
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

        self.bot = bot.AndyBot(self.driver, auth.getDevice())
        for i in range(2):
            self.bot.botSleep(factor=0.02, verbose=True)
            self.bot.driver.unlock()

        # self.theHome()

    def tearDown(self):
        """
        Terminate the application, quit the WebDriver session, and log the test
        completion message.

        This method performs cleanup tasks after test execution, including terminating
        the specified application, quitting the WebDriver session, and logging a
        completion message. If a command-line argument is provided, it additionally
        logs the provided name.

        :raises SystemExit: If there are issues quitting the driver or terminating
            the application.

        :parameter sys.argv: List of command-line arguments where the second argument
            is used as a name for logging purposes.
        :type sys.argv: List[str]

        :return: None
        """
        # self.driver.close_app()
        self.driver.terminate_app("com.instagram.android")
        self.driver.quit()
        if len(sys.argv) > 1:
            nameIs = str(sys.argv[1])
            logg.logSmth(f"\n\n{nameIs}\n\n")
        logg.logSmth("\n\nEND OF TEST\n\n")

    def testRun(self):
        """
        This method runs a test function based on user input or default configuration. It selects a test from a predefined
        set of functions, specifies whether memory writing is required for each function, and logs the results
        of the test execution. In case of an error, an exception is logged, and necessary cleanup operations
        are performed before the method ends.

        :param funcDict: Dictionary mapping test function names to their corresponding functions.
        :type funcDict: dict
        :param memoryWritting: Dictionary indicating whether memory should be written for each function.
        :type memoryWritting: dict
        :param nameIs: String that determines the test function to run, defaults to "theListLike". It can be overridden by
                       the first command-line argument.
        :type nameIs: str
        :raises KeyError: Raised when a function name specified in 'nameIs' is not found in 'funcDict'.
        :raises Exception: Raised if an exception occurs during the execution of the selected test function.
        :raises SystemExit: Raised when necessary operations like memory writing are triggered during cleanup.
        :return: None
        """
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

        nameIs = "theListLike"
        if len(sys.argv) > 1:
            nameIs = str(sys.argv[1])

        print("The test to run is ", nameIs)
        func = funcDict.get(nameIs)
        memoryW = memoryWritting.get(nameIs)

        try:
            func()
        except:
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
        self.bot.theList_Service(numberOfTags=15, numberOfPostsPerTag=5, randomArgs=False, toLike=True, toFollow=False)

    def theList(self):
        self.bot.theList_Service(numberOfTags=18, numberOfPostsPerTag=5, randomArgs=False)

    def theHome(self):
        self.bot.myStats_Service()
        self.bot.homePageScroller(numberOfPosts=120, randomArgs=False)

    def theGame(self):
        # self.bot.myStats_Service()
        self.bot.theGame_Service(numberOfusersToCheck=30, randomArgs=False)

    def theFollowingRecord(self):
        """
        Fetches the list of accounts the user is following, processes the data, and initiates
        a system sleep afterward. This approach assumes interaction with a memory management
        system and account tracking utility to retrieve and manage records of followed users.

        :raises KeyError: Raised if specified keys are not found in the memory file.
        :raises FileNotFoundError: Raised if the memory file is missing or inaccessible.
        :raises Exception: Raised for any generic failure in fetching or processing the data.
        """
        self.bot.memoryManager.readStoredMemoryFile()
        mst.getMyFollowingList(self.bot)  # mode 1

        self.bot.sleep_computer()

    def theFollowingCleanup(self):
        """
        Performs cleanup operations related to the bot's memory and following management. Specifically, it handles
        checking the bot's memory against a list of currently followed accounts to identify inconsistencies,
        and further filters users for additional actions based on certain criteria.

        This function ensures that the memory matches the actual following state of the bot and processes users who
        meet the requirements to undergo an additional automated action.

        :raises ValueError: If a process related to memory fetching or list filtering encounters invalid data.
        """
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

        nameMemory_peopleAlreadyUnfollowed = [y for y in secondDraft_peopleAlreadyUnfollowed]
        filteredList_shouldUnfollow = [x for x in nameMemory_peopleAlreadyUnfollowed if x.handle in mfollowing]

        print(len(filteredList_shouldUnfollow))
        self.gameSortOf(filteredList_shouldUnfollow, self.bot, mfollowing)

        self.bot.sleep_computer()

    def gameSortOf(self, unfollowList, bot, myFollowing):
        """
        Executes the process to unfollow a list of users managed by a given bot. It navigates to
        each user's profile and attempts to unfollow them while handling potential errors such as
        user not being found or loss of internet connection. The function keeps track of unfollow
        statistics and updates the bot's memory and records accordingly. Interactions with the
        bot and logs are used throughout the process for effective task management and debugging.

        :param unfollowList: List of user objects that need to be unfollowed. Each user has properties
            such as a handle to identify their profile.
        :type unfollowList: list

        :param bot: The bot instance responsible for navigating, interacting with users, and maintaining
            records during the unfollowing process.
        :type bot: Bot

        :param myFollowing: List of user handles that the bot is currently following. This list will be
            updated dynamically during the unfollowing process to reflect the current state.
        :type myFollowing: list

        :return: A string indicating an issue encountered during the process (e.g., internet outage
            or shadow ban), or None if the task completed without critical issues.
        :rtype: str or None
        """
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
            logg.logSmth(f"##### - {0} users to be un-Followed")


def main():
    """
    Executes all test cases from the given test class.

    This function creates a test suite by loading all test cases from the
    provided test class using the unittest framework. It then runs the
    test suite with a specified verbosity level using unittest's
    TextTestRunner. The test results, including passed and failed tests,
    are output to the console.

    :return: None
    """
    suite = unittest.TestLoader().loadTestsFromTestCase(test)
    unittest.TextTestRunner(verbosity=1).run(suite)


if __name__ == '__main__':
    main()
