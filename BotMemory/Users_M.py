import json
import time
import AnyBotLog as logg

from datetime import datetime
from uuid import uuid4

timeStampFormat = "%m/%d/%Y, %H:%M:%S"
timeStampFormat_old = "%Y_%m_%d"


# This is a custom encoder class for encoding User_M objects into JSON format
class UserEncoderDecoder(json.JSONEncoder):
    def default(self, us):
        # If the object being encoded is an instance of User_M
        if isinstance(us, User_M):
            # Convert the User_M object into a dictionary with specific key-value pairs
            userDict = {
                '__user__': 'true',
                '0_Handle': us.handle,
                'uid': us.uid,
                # 'Bio': us.bio,
                'AltName': us.altName,
                # 'Stats': us.statsDict,
                # 'StatsTime': us.statsDictTimestamp,
                # 'Past Names': us.listOfPastNames,
                # 'listOf_followers': us.listOf_followers,
                # 'listOf_following': us.listOf_following,
                # 'listOf_HashTagsfollowing': us.listOf_HashTagsfollowing,
                # 'listOf_HashTagsUsing': us.listOf_HashTagsUsing,
                'dateFollowed_byMe': us.dateFollowed_byMe,
                'dateUnFollowed_byMe': us.dateUnFollowed_byMe,
                # 'userIgotYouFrom_youWereFollowing': us._userIgotYouFrom_youWereFollowing,
                'markL0': us._markL0,
                'markL1': us._markL1,
                'markL2': us._markL2,
                'rejected': us._rejected, # rejected - means the profile cannot be found
                # 'dateTimeLovedlast': us._dateTimeLovedlast,
                # 'dateUnLoved_byMe': us.dateUnLoved_byMe,
                # 'dailyLove': us._dailyLove,
                # 'extraLove': us._extraLove
            }
            # Return the dictionary as the JSON object
            return userDict
        # If the object being encoded is not an instance of User_M, use the default JSON encoder
        else:
            return super().default(us)

    # This is a custom decoder function for decoding JSON objects into User_M objects
    def decode_user(dct):
        # If the JSON object has a '__user__' key, it's a User_M object
        if "__user__" in dct:
            # Create a new User_M object and populate its attributes with the values in the dictionary
            user = User_M(dct['0_Handle'])
            user.populate_overwrite(dct)
            return user
        # If the JSON object doesn't have a '__user__' key, it's not a User_M object
        if 'followers' in dct:
            return dct


# This is the User_M class, which represents a user on a social media platform
class User_M:
    # Constructor method for creating a new User_M object
    def __init__(self, handle):
        self.handle = handle
        self.uid = str(uuid4())
        # self.bio = ''  # User Simplification 2023 04 14
        self.altName = ''
        # self.statsDict = []  # contains statsDicts # User Simplification 2023 04 14
        # self.statsDictTimestamp = []  # contains strings of datetime objects
        # self.listOfPastNames = []

        # self.listOf_followers = []
        # self.listOf_following = []
        # self.listOf_HashTagsfollowing = []
        # self.listOf_HashTagsUsing = []

        self.dateFollowed_byMe = None  # The existense of a follow date means that the user has been followed ata some point and could be unfollowed
        self.dateUnFollowed_byMe = None  # The existense of an unfollow date means that the cycle is over. No more follow/unfollow actions for this user
        # self._userIgotYouFrom_youWereFollowing = None

        self._markL0 = False  # MarkL0 means I should investigate this user for L1, and maybe then L2.
        self._markL1 = False  # MarkL1 means this user has fewer followers within a set range and more than X posts.
        self._markL2 = False  # MarkL2 means this user uses hashtags or wording that suggests he/she are interested at a given topic.
        self._rejected = False  # rejected - means the profile cannot be found

        # self._dateTimeLovedlast = None
        # self.dateUnLoved_byMe = None
        # self._dailyLove = False
        # self._extraLove = False

    def populate_overwrite(self, dictio):

        stats = {"posts": 0, "followers": 0, "following": 0}

        if "__user__" in dictio:
            self.handle = dictio.get('0_Handle', ' ')
            self.uid = dictio.get('uid', str(uuid4()))
            # self.bio = dictio.get('Bio', None) # User Simplification 2023 04 14
            self.altName = dictio.get('AltName', None)
            # self.statsDict = dictio.get('Stats', [stats])  # contains statsDicts
            # self.statsDictTimestamp = dictio.get('StatsTime', [])  # contains strings of datetime objects
            # self.listOfPastNames = dictio.get('Past Names', [])
            # self.dateTimeVisitedLast = dictio['LastVisited'] #This will be calculated by dict variable and retrieved only by function

            # User Simplification 2023 04 14
            # self.listOf_followers = dictio.get('listOf_followers', [])
            # self.listOf_following = dictio.get('listOf_following', [])
            # self.listOf_HashTagsfollowing = dictio.get('listOf_HashTagsfollowing', [])
            # self.listOf_HashTagsUsing = dictio.get('listOf_HashTagsUsing', [])

            self.dateFollowed_byMe = dictio.get('dateFollowed_byMe', None)
            self.dateUnFollowed_byMe = dictio.get('dateUnFollowed_byMe', None)
            # self._userIgotYouFrom_youWereFollowing = dictio.get('userIgotYouFrom_youWereFollowing', None)

            self._markL0 = dictio.get('markL0', False)
            self._markL1 = dictio.get('markL1', False)
            self._markL2 = dictio.get('markL2', False)
            self._rejected = dictio.get('rejected', False)

            # self._dateTimeLovedlast = dictio.get('dateTimeLovedlast', None)
            # self.dateUnLoved_byMe = dictio.get('dateUnLoved_byMe', None)
            # self._dailyLove = dictio.get('dailyLove', False)
            # self._extraLove = dictio.get('extraLove', False)

    def updateInfoFromLivePage_Landing(self, userPagePOM):

        # TODO: need to create a routine that compares new userPage stats to old ones
        # in case the userPage belongs to a different user with similar handle (fuzzy matchup and handle changes).
        # this way the new random user will not take the place of an existing entry.
        # The questions is: how  do you handle the case of the above happening? Flash a warning? Does this need manual intervention?

        self.updateHandle(userPagePOM.userName)
        # self.updateStats(userPagePOM.stats)
        self.bio = userPagePOM.bio
        self.altName = userPagePOM.altName
        # self.dateTimeVisitedLast = timestamp #This will be calculated by dict variable and retrieved only by function

    def updateTimelastLoved(self):
        from datetime import datetime
        self._dateTimeLovedlast = datetime.now().strftime(timeStampFormat)

    def updateHandle(self, handleNew):
        # User Simplification 2023 04 14
        # if len(self.listOfPastNames) > 0:
        #     if handleNew != self.listOfPastNames[0]:
        #         self.listOfPastNames.insert(0, self.handle)
        # else:
        #     self.listOfPastNames.insert(0, self.handle)

        self.handle = handleNew

    # User Simplification 2023 04 14
    # def updateStats(self, statsDictIn):
    """This method updates the statsDict and statsDictTimestamp attributes of the object with new stats. If there are already stats 
        in the object, it checks if the new stats are different from the most recent stats. If they are different, it adds the new stats 
        to the beginning of the statsDict list and adds the timestamp of the new stats to the beginning of the statsDictTimestamp list. 
        If the new stats are the same as the most recent stats, it only updates the timestamp of the most recent stats. 
        If there are no stats in the object, it adds the new stats to the beginning of the statsDict list and adds the timestamp of the 
        new stats to the beginning of the statsDictTimestamp list."""

    # User Simplification 2023 04 14
    # from datetime import datetime

    # Check if there are already stats in the object
    # if len(self.statsDict) > 0:
    #     # Check if the new stats are different from the most recent stats
    #     if statsDictIn != self.statsDict[0]:
    #         # If they are different, add the new stats to the beginning of the list
    #         self.statsDict.insert(0, statsDictIn)
    #         # Add the timestamp of the new stats to the beginning of the timestamp list
    #         self.statsDictTimestamp.insert(0, datetime.now().strftime(timeStampFormat))
    #     else:
    #         # If the new stats are the same as the most recent stats, update the timestamp of the most recent stats
    #         self.statsDictTimestamp[0] = datetime.now().strftime(timeStampFormat)
    # else:
    #     # If there are no stats in the object, add the new stats to the beginning of the list
    #     self.statsDict.insert(0, statsDictIn)
    #     # Add the timestamp of the new stats to the beginning of the timestamp list
    #     self.statsDictTimestamp.insert(0, datetime.now().strftime(timeStampFormat))

    # self.statsDict.insert(0, statsDictIn)

    # User Simplification 2023 04 14
    # def getTimeLastVisited(self):
    #     try:
    #         return self.statsDictTimestamp[0]
    #     except Exception as e:
    #         return "01/01/1989, 00:01:01"

    # User Simplification 2023 04 14
    # def getLatestStats(self):
    #     try:
    #         return self.statsDict[0]
    #     except Exception as e:
    #         stats = {
    #             'posts': 0,
    #             'followers': 0,
    #             'following': 0
    #         }
    #         return stats

    # User Simplification 2023 04 14
    # def getLatestPostCount(self):
    #     try:
    #         latestStats = self.getLatestStats()
    #         return latestStats['posts']
    #     except:
    #         return 0

    # User Simplification 2023 04 14
    # def updateHashtagsUsing(self, hashTags):
    #     self.listOf_HashTagsUsing.extend(hashTags)
    #     self.listOf_HashTagsUsing = list(dict.fromkeys(self.listOf_HashTagsUsing))  # remove duplicates

    # User Simplification 2023 04 14
    # def updateHashtagsFollowingList(self, newHashtags):
    #     self.listOf_HashTagsfollowing.extend(newHashtags)
    #     self.listOf_HashTagsfollowing = list(dict.fromkeys(self.listOf_HashTagsfollowing))  # remove duplicates

    # User Simplification 2023 04 14
    # def updateFollowersList(self, listF):
    #     self.listOf_followers.insert(0, listF)

    # User Simplification 2023 04 14
    # def updateFollowingList(self, listF):
    #     self.listOf_following.insert(0, listF)

    def markUserRejected(self):
        self._markL0 = False
        self._rejected = True

    def addToL0(self, sponsorUser):
        self._markL0 = True
        self._userIgotYouFrom_youWereFollowing = sponsorUser

    def addToL1(self):
        if self._markL0:
            self._markL1 = True

    def addToL2(self):
        self._markL2 = True

    def thisUserHasBeenRejected(self):
        return self._rejected

    def markTimeFollowed(self):
        from datetime import datetime
        self._markL0 = False
        self.dateFollowed_byMe = datetime.now().strftime(timeStampFormat)

    def markDateUnfollowed(self):
        from datetime import datetime

        timestamp = datetime.now().strftime(timeStampFormat)
        self.dateUnFollowed_byMe = timestamp

    # User Simplification 2023 04 14
    # def addToLoveDaily(self):
    #     self._dailyLove = True
    #     self._dateTimeLovedlast = "01/01/2020, 14:10:04"
    #
    #     if self.getLatestPostCount() > 0:
    #         self.statsDict[0]['posts'] -= 2  # This is done to make sure the user gets a like the next time I visit

    def addToLoveExtra(self):
        self._extraLove = True
        self._dateTimeLovedlast = "01/01/2020, 14:10:04"
        logg.logSmth(f"#### {self.handle} added to theLoveExtra")

    def removeFromLoveDaily(self):
        timestamp = datetime.now().strftime(timeStampFormat)
        self._dailyLove = False
        self.dateUnLoved_byMe = timestamp

    def removeFromLoveExtra(self):
        self._extraLove = False
        logg.logSmth(f"#### {self.handle} removed from theLoveExtra")

    def daysSinceYouGotFollowed_Unfollowed(self, action, verbose=False):

        # Check if action is "unfollowed" or "followed"
        if "un" in action:
            date = self.dateUnFollowed_byMe
        else:
            date = self.dateFollowed_byMe

        try:
            # Try to parse the date string into a datetime object using the new timestamp format
            startingDate = datetime.strptime(date, timeStampFormat)
        except ValueError:
            # If the new timestamp format doesn't work, try the old format
            startingDate = datetime.strptime(date, timeStampFormat_old)
        except Exception as e:
            # If neither format works, log the error and use the current date and time
            logg.logSmth(e)
            startingDate = datetime.now()

        try:
            # Get the current date and time
            now_DateTime = datetime.now()

            # Convert the starting date and time to Unix timestamp
            d1_ts = time.mktime(startingDate.timetuple())
            # Convert the current date and time to Unix timestamp
            d2_ts = time.mktime(now_DateTime.timetuple())
            # Calculate the difference in days between the two timestamps
            deltaT = int(d2_ts - d1_ts) / 60 / 60 / 24

            if verbose:
                # If verbose mode is on, log the result
                logg.logSmth(f'########## {datetime.today()}:  {str(round(deltaT, 1))} days since I followed {self.handle}')

            return deltaT
        except Exception as e:
            # If there's an error, log it and return 1
            logg.logSmth(e)
            return 1

    def thisUserHasBeenThroughTheSystem(self):
        response = False

        if self.dateFollowed_byMe or self._rejected:
            response = True

        if self._markL1 and self._markL2:
            response = True

        return response

    def thisUserDeservesDailyLove(self):
        return self._dailyLove

    def thisUserDeservesExtraLove(self):
        return self._extraLove

    def thisUserDeservesAnyKindOfLove(self):
        return self.thisUserDeservesDailyLove() or self.thisUserDeservesExtraLove()

    def removeFromLove(self, name="daily"):
        if 'daily' in name:
            self.removeFromLoveDaily()
        elif 'extra' in name:
            self.removeFromLoveExtra()
        else:
            pass

    def iShouldFollowThisUser(self):
        answer = False

        if self._markL1 and self._markL2:
            if not self._rejected and not self.dateFollowed_byMe:
                answer = True

        return answer

    def thereIsNoPointLovingYou(self, userPage):
        if userPage.infoAccess > 45 and userPage.followAccess > 65:
            self.removeFromLove("daily")
            self.removeFromLove("extra")
            logg.logSmth(f"No longer will I love {userPage.userName}")
            return True

    def getSponsor(self):
        return self._userIgotYouFrom_youWereFollowing
