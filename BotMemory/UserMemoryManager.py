import AnyBotLog as logg

import auth
from BotMemory import FileHandlerBot as fh
from BotMemory import Users_M as UM
import time


class UserMemoryManager:
    def __init__(self):
        self.memoryFileHandler = fh.FileHandlerBot()
        self.listOfUserMemory = []
        self.rejected_Users = []

    ### Memory level
    def writeMemoryFileToDrive(self):  # TODO: Re-think when this method is called and if it should always be done explicitly outside this object
        startTime = time.time()

        if len(self.listOfUserMemory) > 3:
            self.slimDownRejectedMemoryRecords()
            self.memoryFileHandler.writeToUserMemory(self.listOfUserMemory, UM.UserEncoderDecoder)

        executionTime = (time.time() - startTime)
        # print('JSON: Execution time in seconds: ' + str(executionTime))

    def pickleMemoryFileToDrive(self):
        startTime = time.time()

        if len(self.listOfUserMemory) > 3:
            self.slimDownRejectedMemoryRecords()
            self.memoryFileHandler.pickleUserMemory(self.listOfUserMemory)

        executionTime = (time.time() - startTime)
        # print('Πίκλα: Execution time in seconds: ' + str(executionTime))

    def writeToIndividualUserMemory(self, userM):
        JSONencoder = UM.UserEncoderDecoder
        file = self.memoryFileHandler.paths['User_Memory'] + userM.uid + '.json'
        self.memoryFileHandler.writeToUserMemory([userM], JSONencoder, file)

    def readStoredMemoryFile(self):  # memory source switch
        # self.readMemoryFileFromDrivePickle()
        self.readMemoryFileFromDriveJSON()

    def readMemoryFileFromDrivePickle(self):
        self.readRejected_Users()

        attemptsAtReadingM = 0
        while len(self.listOfUserMemory) < 3:  # number "3" here is arbitrarily chosen
            attemptsAtReadingM += 1
            self.listOfUserMemory = self.memoryFileHandler.unPickleMemory()

            if attemptsAtReadingM > 2:
                print(f"**** Trouble {attemptsAtReadingM} reading MEMORY FILE FROM DRIVE ****")
            if attemptsAtReadingM > 5:
                print("**** COULD NOT READ MEMORY FILE FROM DRIVE ****")
                raise Exception

        print(f"Succesfully read user memory with {len(self.listOfUserMemory)} users on record")

    def readMemoryFileFromDriveJSON(self):  # JSONdecoder is a function that translates JSON to User_M objects
        self.readRejected_Users()

        JSONdecoder = UM.UserEncoderDecoder.decode_user

        attemptsAtReadingM = 0
        while len(self.listOfUserMemory) < 3:  # number "3" here is arbitrarily chosen
            attemptsAtReadingM += 1
            self.listOfUserMemory = self.memoryFileHandler.readMemoryFile(JSONdecoder)

            if attemptsAtReadingM > 2:
                print(f"**** Trouble {attemptsAtReadingM} reading MEMORY FILE FROM DRIVE ****")
            if attemptsAtReadingM > 5:
                print("**** COULD NOT READ MEMORY FILE FROM DRIVE ****")
                raise Exception

        logg.logSmth(f"Succesfully read user memory with {len(self.listOfUserMemory)} users on record")

        ### Startup routines
        # self.manuallyAddNewUsersTo_theGame()
        # self.redistributeExtraLove()

    def readMemoryFilesFromDrive(self):  # JSONdecoder is a function that translates JSON to User_M objects
        JSONdecoder = UM.UserEncoderDecoder.decode_user
        self.listOfUserMemory = self.memoryFileHandler.readMemoryFiles(JSONdecoder)

    def readRejected_Users(self):
        frame = self.memoryFileHandler.CSV_getFrameFromCSVfile(
            'rejected_UsersCSV')  # TODO: make sure this file is safely written when things break down
        self.rejected_Users = frame['0'].tolist()

    def writeRejected_Users(self):
        frame = self.memoryFileHandler.listToFrame(self.rejected_Users)
        self.memoryFileHandler.CSV_saveFrametoCSVfile('rejected_UsersCSV', frame)

    def getMemoryFile(self):
        return self.listOfUserMemory

    def getDailyLoveList(self):
        daily = [x for x in self.listOfUserMemory if x.thisUserDeservesDailyLove()]
        return daily

    def getExtraLoveList(self):
        extra = [x for x in self.listOfUserMemory if x.thisUserDeservesExtraLove()]
        return extra

    def getListOfSponsorHandles(self):
        sponsorHandles = [x.getSponsor() for x in self.listOfUserMemory]
        sponsorHandles = list(dict.fromkeys(sponsorHandles))
        return sponsorHandles

    def getListOfSponsors(self):
        sponsorHandles = self.getListOfSponsorHandles()
        sponsors = [x for x in self.listOfUserMemory if x.handle in sponsorHandles]
        return sponsors

    def getListOfMarkedUsers(self, number=0):  # 0->L0, 1->L1, 2->L2
        markedUsers = []

        if number == 0:
            markedUsers = [x for x in self.listOfUserMemory if x._markL0]

        if number == 1:
            markedUsers = [x for x in self.listOfUserMemory if x._markL1]

        if number == 2:
            markedUsers = [x for x in self.listOfUserMemory if x._markL2]

        return markedUsers

    def getListOfAllUserHandles(self):
        users = [x.handle for x in self.listOfUserMemory]
        users = list(dict.fromkeys(users))
        return users

    def filterByListOfHandles(self, listOfHandles):
        return [x for x in self.listOfUserMemory if x.handle in listOfHandles]

    # Get list of users to unlove based on number of days before unloving
    def getListOfUsersToUnLove(self, daysBeforeIunLove):
        # Get list of users who have been followed but not unfollowed
        alreadyFollowedOnly = self.getListOfUsersAlreadyFollowedOnly()
        # Filter users who were followed before the specified number of days
        firstDraft = [x for x in alreadyFollowedOnly if x.daysSinceYouGotFollowed_Unfollowed('follow') > daysBeforeIunLove]
        # Filter users who have already been unloved
        return [x for x in firstDraft if not x.dateUnLoved_byMe]

    def getListOfReserveUsersToFollow(self):
        return [x for x in self.listOfUserMemory if x.iShouldFollowThisUser()]

    # Get list of users to unfollow based on number of days before unfollowing
    def getListOfUsersToUnFollow(self, daysBeforeIunFollow):
        # Get list of users who have been followed but not unfollowed
        alreadyFollowedOnly = self.getListOfUsersAlreadyFollowedOnly()

        # Filter users who were followed before the specified number of days
        firstDraft = [x for x in alreadyFollowedOnly if x.daysSinceYouGotFollowed_Unfollowed('follow') > daysBeforeIunFollow]

        # Filter users who have already been unfollowed
        return [x for x in firstDraft if not x.dateUnFollowed_byMe]

    # Get list of users to purge based on number of days since following or unfollowing
    def getListOfUsersToPurgeByDate(self, daysBeforeIunFollow):
        # Get list of users who have been followed or unfollowed
        alreadyFollowed = self.getListOfUsersAlreadyFollowed()
        # Filter users who were followed or unfollowed before the specified number of days
        firstDraft = [x for x in alreadyFollowed if x.daysSinceYouGotFollowed_Unfollowed('follow') > daysBeforeIunFollow]
        # Filter users who were followed or unfollowed more than 120 days ago
        return [x for x in firstDraft if x.daysSinceYouGotFollowed_Unfollowed('follow') < 120]

    # Get list of users who have been followed but not unfollowed
    def getListOfUsersAlreadyFollowedOnly(self):
        alreadyFollowed = [x for x in self.listOfUserMemory if x.dateFollowed_byMe]
        return [x for x in alreadyFollowed if not x.dateUnFollowed_byMe]

    def getListOfUsersAlreadyFollowed(self):
        return [x for x in self.listOfUserMemory if x.dateFollowed_byMe]

    def getListOfRejectedUserHandles(self):
        rejected_in_memory = [x.handle for x in self.listOfUserMemory if x.thisUserHasBeenRejected()]
        rejected_on_file_unique = [x for x in self.rejected_Users if x not in rejected_in_memory]
        rejected = rejected_in_memory + rejected_on_file_unique
        return rejected

    def slimDownRejectedMemoryRecords(self):  # this is not the right way. Users I've added to the love are flagged as rejected

        theListOfRejectedUsersInMemory = [x for x in self.listOfUserMemory if x.thisUserHasBeenRejected()]

        for user in theListOfRejectedUsersInMemory:
            handle = self.slimDownRejectedUserRecord(user)

            if handle not in self.rejected_Users:
                self.rejected_Users.append(handle)

        self.writeRejected_Users()

    def cleanUpMemoryFromNonExistentProfiles(self):
        listToDelete = [x for x in self.listOfUserMemory if (x.bio == '-666' and x.altName == '-666')]
        for user in listToDelete:
            self.removeUserFromRecord(user)

    def manuallyAddNewUsersTo_theGame(self):
        fileOfGameParticipants = self.memoryFileHandler.CSV_getFrameFromCSVfile('addUserTotheGameCSV')['userToAdd'].tolist()  # list of handles
        l0 = [x.handle for x in self.getListOfMarkedUsers(0)]
        newGameParticipants = [x for x in fileOfGameParticipants if x not in l0]
        newGameParticipants = [x for x in newGameParticipants if x not in self.rejected_Users]

        listToReturn = []
        for handle in newGameParticipants:
            user = self.retrieveUserFromMemory(handle)
            if user:
                if not user.thisUserHasBeenThroughTheSystem():
                    user.addToL0(auth.username)
                    user.addToL2()
                    self.updateUserRecord(user)
                    listToReturn.append(user)
            else:
                self.addUserToMemory(handle)
                user = self.retrieveUserFromMemory(handle)
                if user:
                    user.addToL0(auth.username)
                    user.addToL2()
                    self.updateUserRecord(user)
                    listToReturn.append(user)

        return listToReturn

    def redistributeExtraLove(self):
        memoryLoves = [x.handle for x in self.getExtraLoveList()]  # list of handles
        driveLoves = self.memoryFileHandler.CSV_getFrameFromCSVfile('extraLoveCSV')['theLoveExtra'].tolist()  # list of handles

        # Remove dropped users
        droppedLoves = [x for x in memoryLoves if x not in driveLoves]  # list of handles
        for droppedLove in droppedLoves:
            user = self.retrieveUserFromMemory(droppedLove)
            if user:
                user.removeFromLoveExtra()

        # Add new loves
        newDriveLoves = [x for x in driveLoves if x not in memoryLoves]  # list of handles
        for newLove in newDriveLoves:
            user = self.retrieveUserFromMemory(newLove)
            if user:
                user.addToLoveExtra()
            else:
                self.addUserToMemory(newLove)  # this routine adds to both the memory object and writes the whole thing on the drive
                user = self.retrieveUserFromMemory(newLove)
                user.addToLoveExtra()

        # Record current situation
        memoryLoves = [x.handle for x in self.getExtraLoveList()]  # list of handles
        currentLovesDict = {'theLoveExtra': memoryLoves}
        love_frame = self.memoryFileHandler.listToFrame(currentLovesDict)
        self.memoryFileHandler.CSV_saveFrametoCSVfile('extraLoveCSV', love_frame)

    ### User level
    def userExistsInMemory(self, handle):
        flag = False
        for u in self.listOfUserMemory:
            if u.handle == handle:
                flag = True
                break

        return flag

    def userHasBeenRejected(self, handle):
        flag = False
        for u in self.rejected_Users:
            if u == handle:
                flag = True
                break

        return flag

    def retrieveUserFromMemory(self, handle):
        if self.userExistsInMemory(handle):
            userObj = [x for x in self.listOfUserMemory if x.handle == handle][0]
            return userObj
        else:
            return None

    def userPageCannotBeFound(self, user):
        logg.logSmth(f"Dropping user: {user.handle}. No page found (code -666)")
        user.markUserRejected()
        user.removeFromLoveDaily()
        # user.bio = '-666'
        # user.altName = '-666'
        self.updateUserRecord(user)

    def getUID_fromHandle(self, handle):
        userM = self.retrieveUserFromMemory(handle)
        return userM.uid

    def addUserToMemory(self, handleOfNewUser, write=True):
        if not self.userExistsInMemory(handleOfNewUser) and not self.userHasBeenRejected(handleOfNewUser):
            userM = UM.User_M(handleOfNewUser)
            self.listOfUserMemory.append(userM)
            if write:
                self.pickleMemoryFileToDrive()

    def slimDownRejectedUserRecord(self, userObj):
        user = userObj

        userHandle = userObj.handle
        self.removeUserFromRecord(user)

        return userHandle

    def removeUserFromRecord(self, userObj):
        if self.userExistsInMemory(userObj.handle):
            oldUserObj = self.retrieveUserFromMemory(userObj.handle)
            del self.listOfUserMemory[self.listOfUserMemory.index(oldUserObj)]

    def updateUserRecord(self, userObj, writeNow=True):
        if self.userExistsInMemory(userObj.handle):

            # remove old
            self.removeUserFromRecord(userObj)

            # add new
            self.listOfUserMemory.append(userObj)
        else:
            # add new
            if not self.userHasBeenRejected(userObj.handle):
                self.listOfUserMemory.append(userObj)

        if writeNow:
            self.pickleMemoryFileToDrive()
