from POM import Locators as loc
from POM import PostsGrid_POM as grid
from POM import Screen_POM as screen
import auth

from time import sleep


class UserPage(screen.Screen):
    def __init__(self, driver):
        super().__init__(driver)
        self.userName = self.getAttributeBy_ID(loc.userPage_ID['userName'])
        self.altName = self.getAttributeBy_ID(loc.userPage_ID['altName'])
        self.bio = self.getAttributeBy_ID(loc.userPage_ID['bio'])
        self.getStats_dict()

        self.determineLevelOfFollowAccess()
        self.infoAccess = 50  # switch with the line below if you need more info
        # self.determineLevelOfInfoAccess()

        self.grid = None

    def getAttributeBy_ID(self, locatorID):
        attr = None
        element = self.findElementBy_ID(locatorID)
        if element:
            attr = element.text

        if not attr:
            print(f"Could not find {locatorID} on userpage for {self.userName}")

        return attr

    def getStats_dict(self):
        self.stats = {
            'posts': 0,
            'followers': 0,
            'following': 0
        }

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

        self.followAccess = 0
        if self.userName == auth.username:
            return
        else:
            self.followAccess += 20  # @20

        # Ok so it is NOT me.
        # One step further away from me are people I am following. Check for that
        try:
            # @20
            self.driver.find_element_by_xpath(loc.userPage_XPATH['Button_Following'])
            return
        except Exception as e:
            self.followAccess += 20  # @40

        # Ok so it is NOT someone I am following.
        # One step further away from me are people I have requested to follow. Check for that
        try:
            # @40
            self.driver.find_element_by_xpath(loc.userPage_XPATH['Button_Requested'])
            return
        except Exception as e:
            self.followAccess += 20  # @60

        # If we get to this point it turns out to be someone I am not following at all,
        # and neither have requested to follow. Do THEY follow me though?
        try:
            # @60
            self.driver.find_element_by_xpath(loc.userPage_XPATH['Button_FollowBack'])
            return
        except Exception as e:
            self.followAccess += 10  # @70

        try:
            # @70
            self.driver.find_element_by_xpath(loc.userPage_XPATH['Button_Follow'])
            return
        except Exception as e:
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
            self.driver.find_element_by_id(loc.userPage_ID['EmptyProfileNotice'])
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
        print('~~> {0}'.format(self.get_profileTypeDescription()))

    def follow(self):
        self.determineLevelOfFollowAccess()
        if self.followAccess > 45:
            try:
                followButton = self.findElementBy_XPATH(loc.userPage_XPATH['Button_Follow'])
                followButton.click()

            except Exception as e:
                print('Cannot find the follow button')

            sleep(2)
            self.determineLevelOfFollowAccess()

            if self.followAccess < 45:
                print('#### OK followed {}'.format(self.userName))
                return 'OK'
            else:
                return 'fail'
        else:
            print('#### nahh - no follow access for this user because:')
            self.printProfileTypeDescription()
            return 'OK'

    def unfollow(self):
        self.determineLevelOfFollowAccess()
        if 45 > self.followAccess > 5:
            if self.followAccess < 25:
                # if following
                self.findElementBy_XPATH(loc.userPage_XPATH['Button_Following']).click()
                sleep(2)
                self.findElementBy_ID(loc.userPage_ID['UnfollowSecond']).click()
                sleep(2)

                # if their profile is private and Insta warns I would need to request access if I Unfollow
                # thereIsAFinalButton = self.findElementBy_ID(loc.userPage_ID['UnfollowFinal'])
                # if thereIsAFinalButton:
                #     thereIsAFinalButton.click()

            else:
                # if requested
                self.findElementBy_XPATH(loc.userPage_XPATH['Button_Requested']).click()
                sleep(2)
                self.findElementBy_ID(loc.userPage_ID['UnfollowSecond']).click()
                sleep(2)

                # if their profile is private and Insta warns I would need to request access if I Unfollow
                thereIsAFinalButton = self.findElementBy_ID(loc.userPage_ID['UnfollowFinal'])
                if thereIsAFinalButton:
                    thereIsAFinalButton.click()

            self.determineLevelOfFollowAccess()
            if self.followAccess > 45:
                print('#### OK UNfollowed {}'.format(self.userName))
                self.printProfileTypeDescription()
                return 'OK'
            else:
                return 'fail'
        else:
            print('#### nahh - no unfollow access for this user because:')
            self.printProfileTypeDescription()
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
