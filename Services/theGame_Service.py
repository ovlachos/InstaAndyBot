import AnyBotLog as logg
from BotMemory import InfidelsList


def playTheGame(bot, num):
    logg.logSmth("#" * 40)
    logg.logSmth(" " * 10 + "*" * 5 + " The Game " + "*" * 5 + " " * 10)
    logg.logSmth("#" * 40)

    # ~~ Read User Memory
    bot.memoryManager.readStoredMemoryFile()
    # bot.memoryManager.readMemoryFileFromDrivePickle()

    # ~~ Update My Stats
    bot.myStats_Service()

    # ~~ Derive User Lists
    unfollowList = bot.memoryManager.getListOfUsersToUnFollow(bot.daysBeforeIunFollow)  # [:num]
    manuallyAddedList = bot.memoryManager.manuallyAddNewUsersTo_theGame()
    reservesList = None  # bot.memoryManager.getListOfReserveUsersToFollow()[:num]
    unLoveList = None  # bot.memoryManager.getListOfUsersToUnLove(bot.daysBeforeIunLove)
    purgeList = None  # InfidelsList.infidels  # manually curated

    # ~~ Un Love ###
    if unLoveList:
        logg.logSmth(f"##### - {len(unLoveList)} users to be un-Loved")
        for user in unLoveList:
            user.removeFromLoveDaily()
            bot.memoryManager.updateUserRecord(user, False)
        bot.memoryManager.pickleMemoryFileToDrive()
    else:
        logg.logSmth("##### - 0 users to be un-Loved")

    # ~~ Un Follow ###
    if not unfollowList:
        logg.logSmth('##### - 0 users to be un-Followed')
    else:
        logg.logSmth(f"##### - {len(unfollowList)} users to be un-Followed")
        unfollowListProcess(bot, unfollowList)

    # ~~ Purge ### MANUALLY
    if not purgeList:
        logg.logSmth('##### - 0 infidels to be Purged (by manual selection)')
    else:
        logg.logSmth(f"##### - {len(purgeList)} users to be un-Followed")
        purgeListProcess(bot, purgeList)

    # ~~ USERS MANUALLY ADDED
    if not manuallyAddedList or bot.followMana < 0:
        logg.logSmth('##### - 0 manually added users to be Followed')
    else:
        followManuallyAddedProccess(bot, manuallyAddedList)

    return "OK"


def L1_criteria(userStats, myFollowers):
    # Filter out users with more followers than myself, 0 posts etc.- aka L1
    followerCountLimit = myFollowers

    if (
            userStats['followers'] > (1.05 * followerCountLimit)
            or userStats['followers'] < 100
            or userStats['posts'] < 3
    ):
        wording = 'Dropping'
    else:
        wording = 'Keeping'

    return "Dropping" not in wording


def unfollowListProcess(bot, unfollowList):
    unfollow_counter = 0

    # Go through the list of users to unfollow
    for user in unfollowList:
        user.daysSinceYouGotFollowed_Unfollowed('follow', True)

        userPage = userPageNavigation(bot, user)
        if not userPage:
            continue

        logg.logSmth(f"########## Will unfollow user {user.handle}")

        if 'OK' in userPage.unfollow():
            user.markDateUnfollowed()
            bot.memoryManager.updateUserRecord(user)

            unfollow_counter += 1
            logg.logSmth(f"##### {unfollow_counter} / {len(unfollowList)} users unfollowed today")

            bot.botSleep()


def purgeListProcess(bot, purgeList):
    '''
    An unfollow process that does not involve reading/writing to memory
    Mainly for manually added lists of profiles
    '''
    unfollow_counter = 0

    # Go through the list of users to unfollow
    for user in purgeList:

        userPage = userPageNavigation(bot, user)
        if not userPage:
            continue

        logg.logSmth(f"########## Will unfollow user {user.handle}")

        if 'OK' in userPage.unfollow():
            unfollow_counter += 1
            logg.logSmth(f"##### {unfollow_counter} / {len(purgeList)} users unfollowed today")

            bot.botSleep()


def followManuallyAddedProccess(bot, manuallyAddedList):
    # reduce size to available follow mana
    manuallyAddedList = manuallyAddedList[:bot.followMana]
    logg.logSmth(f"##### - {len(manuallyAddedList)} manually added users to be Inspected/Followed")

    userNotFound_counter = 0
    for user in manuallyAddedList:
        logg.logSmth(f"########## Navigating to user {user.handle}")
        searchPage = bot.navRibons.goToSearchPage()
        userPage = searchPage.navigateToUserPage(user.handle)

        if not userPage:
            bot.memoryManager.userPageCannotBeFound(user)

            userNotFound_counter += 1
            if userNotFound_counter > 3:
                return "No Internet - ...or search shadow ban"

            continue

        userNotFound_counter = 0  # restart this counter as we only want to see if we fail to get X users in a row, before shuting things down

        # check L1
        # if L1_criteria(userPage.stats, bot.ownFollowers):
        user.addToL1()

        if user.iShouldFollowThisUser() and bot.followMana > 0:
            logg.logSmth(f"########## Will follow user {user.handle}", 'INFO')
            if 'OK' in userPage.follow():
                user.markTimeFollowed()
                user.addToLoveDaily()
                bot.decrementFolowMana(1)
        else:
            logg.logSmth(f"########## Manually added user {user.handle} not worthy", 'INFO')

        bot.memoryManager.updateUserRecord(user)
        if user.dateFollowed_byMe:
            bot.botSleep()


def userPageNavigation(bot, user):
    searchPage = None
    while not searchPage:
        searchPage = bot.navRibons.goToSearchPage()
        if not searchPage:
            bot.navRibons.goBack()

    if userPage := searchPage.navigateToUserPage(user.handle):
        return userPage

    bot.memoryManager.userPageCannotBeFound(user)
    return None
