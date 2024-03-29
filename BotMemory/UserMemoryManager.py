import time

import AnyBotLog as logg
import auth
from BotMemory import FileHandlerBot as fh
from BotMemory import Users_M as UM


class UserMemoryManager:
    def __init__(self):
        self.memoryFileHandler = fh.FileHandlerBot()
        self.listOfUserMemory = []
        self.rejected_Users = []

    ### Memory level
    def writeMemoryFileToDrive(
            self):  # TODO: Re-think when this method is called and if it should always be done explicitly outside this object
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
        try:
            a=1
        finally:
            frame = self.memoryFileHandler.listToFrame(self.rejected_Users)
            self.memoryFileHandler.CSV_saveFrametoCSVfile('rejected_UsersCSV', frame)
            # logg.logSmth("Rejected users, written to file")

    def getMemoryFile(self):
        return self.listOfUserMemory

    def getDailyLoveList(self):
        return [x for x in self.listOfUserMemory if x.thisUserDeservesDailyLove()]

    def getExtraLoveList(self):
        return [x for x in self.listOfUserMemory if x.thisUserDeservesExtraLove()]

    def getListOfSponsorHandles(self):
        sponsorHandles = [x.getSponsor() for x in self.listOfUserMemory]
        sponsorHandles = list(dict.fromkeys(sponsorHandles))
        return sponsorHandles

    def getListOfSponsors(self):
        sponsorHandles = self.getListOfSponsorHandles()
        return [x for x in self.listOfUserMemory if x.handle in sponsorHandles]

    def getListOfMarkedUsers(self, number=0):  # 0->L0, 1->L1, 2->L2
        markedUsers = []

        if number == 0:
            markedUsers = [x for x in self.listOfUserMemory if x._markL0]

        elif number == 1:
            markedUsers = [x for x in self.listOfUserMemory if x._markL1]

        elif number == 2:
            markedUsers = [x for x in self.listOfUserMemory if x._markL2]

        return markedUsers

    def getListOfAllUserHandles(self):
        users = [x.handle for x in self.listOfUserMemory]
        return list(dict.fromkeys(users))

    def filterByListOfHandles(self, listOfHandles):
        return [x for x in self.listOfUserMemory if x.handle in listOfHandles]

    # Get list of users to unlove based on number of days before unloving
    def getListOfUsersToUnLove(self, daysBeforeIunLove):
        # Get list of users who have been followed but not unfollowed
        alreadyFollowedOnly = self.getListOfUsersAlreadyFollowedOnly()
        # Filter users who were followed before the specified number of days
        firstDraft = [x for x in alreadyFollowedOnly if
                      x.daysSinceYouGotFollowed_Unfollowed('follow') > daysBeforeIunLove]
        # Filter users who have already been unloved
        return [x for x in firstDraft if not x.dateUnLoved_byMe]

    def getListOfReserveUsersToFollow(self):
        return [x for x in self.listOfUserMemory if x.iShouldFollowThisUser()]

    # Get list of users to unfollow based on number of days before unfollowing
    def getListOfUsersToUnFollow(self, daysBeforeIunFollow):
        # Get list of users who have been followed but not unfollowed
        alreadyFollowedOnly = self.getListOfUsersAlreadyFollowedOnly()

        # Filter users who were followed before the specified number of days
        firstDraft = [x for x in alreadyFollowedOnly if
                      x.daysSinceYouGotFollowed_Unfollowed('follow') > daysBeforeIunFollow]

        # Filter users who have already been unfollowed
        return [x for x in firstDraft if not x.dateUnFollowed_byMe]

    # Get list of users to purge based on number of days since following or unfollowing
    def getListOfUsersToPurgeByDate(self, daysBeforeIunFollow):
        # Get list of users who have been followed or unfollowed
        alreadyFollowed = self.getListOfUsersAlreadyFollowed()
        # Filter users who were followed or unfollowed before the specified number of days
        firstDraft = [x for x in alreadyFollowed if
                      x.daysSinceYouGotFollowed_Unfollowed('follow') > daysBeforeIunFollow]
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
        return rejected_in_memory + rejected_on_file_unique

    def slimDownRejectedMemoryRecords(
            self):  # this is not the right way. Users I've added to the love are flagged as rejected

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
        fileOfGameParticipants = self.memoryFileHandler.CSV_getFrameFromCSVfile('addUserTotheGameCSV')[
            'userToAdd'].tolist()  # list of handles
        l0 = [x.handle for x in self.getListOfMarkedUsers(0)]
        newGameParticipants = [x for x in fileOfGameParticipants if x not in l0]
        newGameParticipants = [x for x in newGameParticipants if x not in self.rejected_Users]

        listToReturn = []
        for handle in newGameParticipants:
            if user := self.retrieveUserFromMemory(handle):
                if not user.thisUserHasBeenThroughTheSystem():
                    self._extracted_from_manuallyAddNewUsersTo_theGame_12(user, listToReturn)
            else:
                self.addUserToMemory(handle)
                if user := self.retrieveUserFromMemory(handle):
                    self._extracted_from_manuallyAddNewUsersTo_theGame_12(user, listToReturn)
        return listToReturn

    # TODO Rename this here and in `manuallyAddNewUsersTo_theGame`
    def _extracted_from_manuallyAddNewUsersTo_theGame_12(self, user, listToReturn):
        user.addToL0(auth.username)
        user.addToL2()
        self.updateUserRecord(user)
        listToReturn.append(user)

    def redistributeExtraLove(self):
        memoryLoves = [x.handle for x in self.getExtraLoveList()]  # list of handles
        driveLoves = self.memoryFileHandler.CSV_getFrameFromCSVfile('extraLoveCSV')[
            'theLoveExtra'].tolist()  # list of handles

        # Remove dropped users
        droppedLoves = [x for x in memoryLoves if x not in driveLoves]  # list of handles
        for droppedLove in droppedLoves:
            if user := self.retrieveUserFromMemory(droppedLove):
                user.removeFromLoveExtra()

        # Add new loves
        newDriveLoves = [x for x in driveLoves if x not in memoryLoves]  # list of handles
        for newLove in newDriveLoves:
            user = self.retrieveUserFromMemory(newLove)
            if not user:
                self.addUserToMemory(
                    newLove)  # this routine adds to both the memory object and writes the whole thing on the drive
                user = self.retrieveUserFromMemory(newLove)
            user.addToLoveExtra()
        # Record current situation
        memoryLoves = [x.handle for x in self.getExtraLoveList()]  # list of handles
        currentLovesDict = {'theLoveExtra': memoryLoves}
        love_frame = self.memoryFileHandler.listToFrame(currentLovesDict)
        self.memoryFileHandler.CSV_saveFrametoCSVfile('extraLoveCSV', love_frame)

    ### User level
    def userExistsInMemory(self, handle):
        return any(u.handle == handle for u in self.listOfUserMemory)

    def userHasBeenRejected(self, handle):
        return any(u == handle for u in self.rejected_Users)

    def retrieveUserFromMemory(self, handle):
        if self.userExistsInMemory(handle):
            return [x for x in self.listOfUserMemory if x.handle == handle][0]
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
        elif not self.userHasBeenRejected(userObj.handle):
            self.listOfUserMemory.append(userObj)

        if writeNow:
            self.pickleMemoryFileToDrive()

#TODO:
"""

Time for a database. What kind of file? .CSV? SQL .db? .json? pickle?
Do I really need to manually read and edit the entries of the database? Not if it is working as intended. I can always do that programmatically.
Go for SQL, or smth more modern then?
What do I need from my DB to store:
    USERS:
    ~ User name
    ~ Time visited last
    ~ Entry creation date (i.e. first time visited)
    ~ Followed date
    ~ UnFollowed date

    Table follows {
      following_user_id integer
      followed_user_id integer
      created_at timestamp 
    }   

    Table users {
      id integer [primary key]
      username varchar
      rejected boolean //Only if profile cannot be found
      created_at timestamp
      folowed_date timestamp
      unfolowed_date timestamp
    }

    Table posts {
      id integer [primary key]
      body text [note: 'Content of the post']
      user_id integer
      updated_at timestamp
    }

    Table interactions {
      liked_user_id integer
      commented_user_id integer
    }

A graph database looks promising for the user interconnection exploration.  https://graph-tool.skewed.de/
What kind of edges or relationships do users have with each other? graph = edge = relationship and can be labeled, directed, assigned properties.
A user :
    ~ Is Followed by and/or following (other user: OU) [two-way edge] :: path metadata 
    ~ Likes a Post (weak) of OU [one-way edge] :: path metadata/properties
    ~ Comments on a post of OU [one-way edge] :: path metadata/properties
    ~ Is tagged on a post of OU [one-way edge] :: path metadata/properties
    ~ Is a post co-author, collaborator [two-way edge] :: path metadata/properties = how many collabs
    ~ Posts a post
    
    ~ Has a handle/username
    ~ Has a Time visited last
    ~ Has an Entry creation date (i.e. first time visited)
    ~ Has a Followed date
    ~ Has an UnFollowed date
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    The simplest way to think about relationships is to just write declarative sentences about our domain.
    Write some true facts, and isolate the “nouns” (in bold) and “verbs” (in italics). Example:

    A person posts an article
    A person friends another person
    A person has an interest

    In this simplified view of the domain, all of your nouns are nodes, and all of your relationships are verbs. 
    The relationship type is the singular form of the verb. And so this implies a graph that 
    looks like (:Person)-[:POSTS]->(:Article) and so on.
    Under the simple explanation, the task is to decompose your domain into a large batch of simple declarative sentences. 
    This gives you a pile of nodes and relationships to work with. You then have most of your model, 
    and mostly have to make naming decisions.
    
    Network/ graph density: How many edges exist compared to how many could exist (i.e. how saturated the network is). 1 for everyone being connected to everyone else, 0 for no connections at all, 0 edges.
    Node degree: How many edges a node has. Metric of centrality, the more edges (connections) a node has the more central, or "popular" is is.
    Clustering coefficient: 
    Modularity: the number of sub-communities within a group  
    
    LookUp TypeDB tutorials
"""
