import random

import auth

from time import sleep
import AnyBotLog as logg

from POM import Locators as loc
from POM import PostsGrid_POM as grid
from POM import Screen_POM as screen


class UserPage(screen.Screen):
    def __init__(self, driver):
        super().__init__(driver)

        # Get user information from the page
        self.userName = self.getAttributeBy_ID(loc.userPage_ID['userName'])
        self.altName = ''  # self.getAttributeBy_ID(loc.userPage_ID['altName'])
        self.bio = ''  # self.getAttributeBy_ID(loc.userPage_ID['bio'])

        # Get user statistics (number of posts, followers, and following)
        self.getStats_dict()

        # Determine the level of access the user has for following and user information
        self.determineLevelOfFollowAccess()
        self.infoAccess = 50  # switch with the line below if you need more info
        # self.determineLevelOfInfoAccess()

        # Initialize grid variable to be used later
        self.grid = None

    # Verify if the current page is a user page and if the user statistics have been obtained
    def verifyPageType(self):
        if self.stats:
            return True
        return False

    # Verify if the user information (username) is present
    def verifyUser(self, handle=None):
        if not self.verifyPageType():
            logg.logSmth('##### Are you in a user page for sure?', 'WARNING')
            return False

        logg.logSmth(F'##### User name title {self.userName}', 'INFO')
        return True

    # Get an attribute of the user page by its ID
    def getAttributeBy_ID(self, locatorID):
        attr = None
        element = self.findElementBy_ID(locatorID)
        if element:
            attr = element.text

        # Log a message if the attribute could not be found
        try:
            if not attr:
                logg.logSmth(f"Could not find {locatorID} on userpage for {self.userName}", 'INFO')
        except Exception as e:
            logg.logSmth(f"Error getting userPage attribute {e} ", 'WARNING')

        return attr

    # Get user statistics (number of posts, followers, and following)
    def getStats_dict(self):
        self.stats = {
            'posts': 0,
            'followers': 0,
            'following': 0
        }

        # Helper function to refine the counts obtained from the user page
        def refineCounts(countStr):
            if 'M' in countStr:
                countStr = countStr.split('M')[0]
                txtInt = float(countStr) * 1E6
                txtInt = int(txtInt)
            elif 'K' in countStr:
                countStr = countStr.split('K')[0]
                txtInt = float(countStr) * 1E3
                txtInt = int(txtInt)
            elif ',' in countStr:
                txtInt = countStr.replace(',', '')
                txtInt = int(txtInt)
            else:
                txtInt = int(countStr)

            return txtInt

        # Get the number of posts, followers, and following
        posts = self.findElementBy_ID(loc.userPage_ID['postsCount'])
        if posts:
            self.stats['posts'] = refineCounts(posts.text)

        followers = self.findElementBy_ID(loc.userPage_ID['followersWindow'])
        if followers:
            self.stats['followers'] = refineCounts(followers.text)

        following = self.findElementBy_ID(loc.userPage_ID['followingWindow'])
        if following:
            self.stats['following'] = refineCounts(following.text)

    def determineLevelOfFollowAccess(self):
        # Follow Access:
        # 0  -  A: It is me
        # 20 -  B: It's someone I'm following currently
        # 40 -  C: It's someone I've requested to follow (and they have not yet replied)
        # 60 -  D: It's someone I do not follow
        # 70 -  E: It's someone I unfollowed and he still follows
        # 80 -  F: It's someone I unfollowed but he did NOT follow back

        """I need to make this faster somehow. Less findBy_XPATH calls"""

        self.followAccess = 0
        if self.userName == auth.username:
            return
        else:
            self.followAccess += 20  # @20

        # Ok so it is NOT me.
        # One step further away from me are people I am following. Check for that
        if self.findElementBy_XPATH(loc.userPage_XPATH['Button_Following']):
            return  # @20
        else:
            self.followAccess += 20  # @40

        # Ok so it is NOT someone I am following.
        # One step further away from me are people I have requested to follow. Check for that
        if self.findElementBy_XPATH(loc.userPage_XPATH['Button_Requested']):
            return  # @40
        else:
            self.followAccess += 20  # @60

        # If we get to this point it turns out to be someone I am not following at all,
        # and neither have requested to follow. Do THEY follow me though?
        if self.findElementBy_XPATH(loc.userPage_XPATH['Button_FollowBack']):
            return  # @60
        else:
            self.followAccess += 10  # @70

        if self.findElementBy_XPATH(loc.userPage_XPATH['Button_Follow']):
            return  # @70
        else:
            self.followAccess += 10  # @80

    def determineLevelOfInfoAccess(self):
        # Info/lists Access:
        # 0  - 01: It is me
        # 25 - 02: It is an open profile. I have access to info/lists/posts
        # 50 - 03: It is a private profile. Limited access

        self.infoAccess = 0

        if self.userName == auth.username:
            return
        else:
            self.infoAccess += 25  # @25

        # If it's not me it could either be an open or private profile. Let us check for that.
        try:
            self.findElementBy_ID(loc.userPage_ID['EmptyProfileNotice'])
            self.infoAccess += 25  # @50
        except Exception as e:
            pass
            # self.infoAccess = 100

    def get_profileTypeDescription(self):
        # phrased so that it fits in 'This user BLAH ...'
        descriptionInfoAccess = {
            '0': 'full access since this is myself! good job finding me :P',
            '25': 'full access',
            '50': 'limited access to just the basics',
            '100': 'no access. Is this an error page?',
        }

        descriptionFollowAccess = {
            '0': 'cannot follow myself i.e.',
            '20': 'am already following',
            '40': 'have requested to follow',
            '60': 'am not following, but I am being followed by',
            '70': 'am not following',
            '100': 'no access. Is this an error page?',
        }
        return f"I {descriptionFollowAccess[str(self.followAccess)]} user {self.userName} and I have {descriptionInfoAccess[str(self.infoAccess)]}"  # description[str(self.type)]

    def printProfileTypeDescription(self):
        logg.logSmth(f'~~~~~~~~~> {self.get_profileTypeDescription()}')

    def get_followers_list(self, percentage=1):
        page = self.navToFolowers()

        logg.logSmth(f"I am getting my followers for a count of {int(self.stats['followers'] * percentage)} and a percentage of {percentage}")
        self.followers = page.getListOfUsers(int(self.stats['followers'] * percentage))

    def get_following_list(self, percentage=1):
        page = self.navToFolowing()
        page.reactionWait()

        # Sort by 'earliest'
        for i in range(2):
            randParam = random.choice(['following_sorting_option_latest', 'following_sorting_option_default'])
            page.getAndClickElementBy_ID(loc.userPage_ID.get('followingSortingButton'))
            page.getAndClickElementBy_XPATH(loc.userPage_XPATH.get('following_sorting_option_latest'))
            page.reactionWait(.5)

            page.getAndClickElementBy_ID(loc.userPage_ID.get('followingSortingButton'))
            page.getAndClickElementBy_XPATH(loc.userPage_XPATH.get('following_sorting_option_earliest'))
            page.reactionWait(.5)

        logg.logSmth(f"I am getting my following for a count of {int(self.stats['following'] * percentage)} and a percentage of {percentage}")
        self.following = page.getListOfUsers(int(self.stats['following'] * percentage))

    def get_following_hashTag_list(self):
        page = self.navToFolowingHashTags()
        self.folowingHashTags = []
        if page:
            self.folowingHashTags = page.getListOfHashtags()

    def follow(self):
        self.determineLevelOfFollowAccess()
        if self.followAccess > 45:
            try:
                followButton = self.findElementBy_XPATH(loc.userPage_XPATH['Button_Follow'])
                followButton.click()

            except Exception as e:
                logg.logSmth(f'Cannot find the follow button for {self.userName}', 'WARNING')

            sleep(2)
            self.determineLevelOfFollowAccess()

            if self.followAccess < 45:
                logg.logSmth('########## OK followed {}'.format(self.userName), 'INFO')
                return 'OK'
            else:
                return 'fail'
        else:
            # logg.logSmth('########## nahh - no follow access for this user because:')
            # self.printProfileTypeDescription()
            return 'ΝΟΤ'  # TODO although already followed or requested this result still subtracts from daily follow mana

    def unfollow(self):
        # Determine level of follow access for the user
        self.determineLevelOfFollowAccess()

        # If we have enough access to unfollow
        if 45 > self.followAccess > 5:
            # If the follow access is less than 25, the user is being followed
            if self.followAccess < 25:
                # Unfollow the user
                self.findElementBy_XPATH(loc.userPage_XPATH['Button_Following']).click()
                sleep(2)
                self.findElementBy_ID(loc.userPage_ID['UnfollowSecond']).click()
                sleep(2)

                # If their profile is private and Instagram warns we would need to request access if we unfollow
                try:
                    is_there_a_final_button = self.findElementBy_ID(loc.userPage_ID['UnfollowFinal'])
                    if is_there_a_final_button:
                        is_there_a_final_button.click()
                except:
                    pass
            else:
                # If the user has been requested to follow
                self.findElementBy_XPATH(loc.userPage_XPATH['Button_Requested']).click()
                sleep(2)
                self.findElementBy_ID(loc.userPage_ID['UnfollowSecond']).click()
                sleep(2)

                # If their profile is private and Instagram warns we would need to request access if we unfollow
                there_is_a_final_button = self.findElementBy_ID(loc.userPage_ID['UnfollowFinal'])
                if there_is_a_final_button:
                    there_is_a_final_button.click()

            # Determine the level of follow access again
            self.determineLevelOfFollowAccess()

            # If we successfully unfollowed the user
            if self.followAccess > 45:
                logg.logSmth('########## OK UNfollowed {}'.format(self.userName), 'INFO')
                self.printProfileTypeDescription()
                return 'OK'
            else:
                return 'fail'
        else:
            # We don't have enough access to unfollow the user
            # logg.logSmth('########## nahh - no unfollow access for this user because:')
            # self.printProfileTypeDescription()
            return 'OK'

    def bringUpPostGrid(self):
        postButton = self.findElementBy_ID(loc.userPage_ID['postsCount'])
        if postButton:
            postButton.click()
            sleep(2)
            self.grid = grid.PostGrid(self.driver)

    def likeUserPostByOrder(self, order):
        self.bringUpPostGrid()
        self.grid.likePostByOrder(order)
        self.driver.back()
        return UserPage(self.driver)

    def navToFolowers(self):
        followersCount = self.findElementBy_ID(loc.userPage_ID['followersWindow'])
        if followersCount:
            followersCount.click()
            return followListPage(self.driver)

    def navToFolowing(self):
        followingCount = self.findElementBy_ID(loc.userPage_ID['followingWindow'])
        if followingCount:
            followingCount.click()
            return followListPage(self.driver)

    def navToFolowingHashTags(self):
        if self.getAndClickElementBy_ID(loc.userPage_ID['followingWindow']):
            if self.getAndClickElementBy_ID(loc.userPage_ID['followingHashTagWindow']):
                return followListPage(self.driver)

    def openMuteDialogue(self):
        self.determineLevelOfFollowAccess()
        if 45 > self.followAccess > 5:
            if self.followAccess < 25:
                # if following
                self.findElementBy_XPATH(loc.userPage_XPATH['Button_Following']).click()
                sleep(2)
                self.findElementBy_ID(loc.userPage_ID['MuteButton']).click()

    def mutePosts(self):
        self.findElementBy_ID(loc.userPage_ID['MutePosts']).click()

    def muteStories(self):
        self.findElementBy_ID(loc.userPage_ID['MuteStories']).click()

    def muteReels(self):
        pass

    def MuteAll(self, posts=True, stories=True):
        if posts or stories:
            self.openMuteDialogue()

            if posts:
                self.mutePosts()
            if stories:
                self.muteStories()

            # logg.logSmth('########## OK Muted {}'.format(self.userName), 'INFO')
        # self.muteReels()


class followListPage(screen.Screen):
    def __init__(self, driver):
        super().__init__(driver)

    def typeIntoSearchField(self, query, speed='slow'):
        textBox = self.findElementBy_ID(loc.userPage_ID['followingSearchField'])
        if textBox:
            if 'slow' in speed:
                self.slowType(query, textBox)
                self.driver.back()
            else:
                self.fastType(query, textBox)

    def verify_if_user_in_list(self):
        pass

    def getListOfUsers(self, expectedCount):
        listOfUsers = []
        firstView = self.findElementsBy_ID(loc.userPage_ID['followingSearchResult'])
        firstView = [x.text for x in firstView]
        listOfUsers.extend(firstView)

        logCounter = 0
        while len(listOfUsers) <= 0.99 * expectedCount:
            self.vSwipeUp('small')
            allOtherViews = self.findElementsBy_ID(loc.userPage_ID['followingSearchResult'])
            allOtherViews = [x.text for x in allOtherViews]
            listOfUsers.extend(allOtherViews)
            listOfUsers = list(dict.fromkeys(listOfUsers))  # removes duplicates

            logCounter += 1
            if logCounter % 5 == 0:
                logg.logSmth(f"I got {len(listOfUsers)} users so far")

        return listOfUsers

    def getListOfHashtags(self):
        listOfTags = []
        firstView = self.findElementsBy_ID(loc.userPage_ID['followingHashTagSearchResult'])
        firstView = [x.text for x in firstView]
        listOfTags.extend(firstView)

        arbitraryCounter = 0
        while arbitraryCounter <= 5:
            self.vSwipeUp('tiny')
            allOtherViews = self.findElementsBy_ID(loc.userPage_ID['followingHashTagSearchResult'])
            allOtherViews = [x.text for x in allOtherViews]
            listOfTags.extend(allOtherViews)
            listOfTags = list(dict.fromkeys(listOfTags))  # removes duplicates
            arbitraryCounter += 1

        return listOfTags
