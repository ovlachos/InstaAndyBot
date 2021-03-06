import AnyBotLog as logg


def playTheGame(bot, num):
    logg.logSmth(f"#" * 40)
    logg.logSmth(f" " * 10 + "*" * 5 + " The Game " + "*" * 5 + " " * 10)
    logg.logSmth(f"#" * 40)

    ### Read User Memory
    bot.memoryManager.readMemoryFileFromDriveJSON()

    # bot.memoryManager.readMemoryFileFromDrivePickle()
    # handle =bot.memoryManager.getUID_fromHandle('tooironictospeak')
    # print(f"Handle is: {handle} tooironictospeak")

    ### Derive Lists
    reservesList = bot.memoryManager.getListOfReserveUsersToFollow()[:num]
    unfollowList = bot.memoryManager.getListOfUsersToUnFollow(bot.daysBeforeIunFollow)  # [:num]
    unLoveList = bot.memoryManager.getListOfUsersToUnLove(bot.daysBeforeIunLove)
    manuallyAddedList = bot.memoryManager.manuallyAddNewUsersTo_theGame()

    ### Un Love ###
    if unLoveList:
        logg.logSmth(f"##### - {len(unLoveList)} users to be un-Loved")
        for user in unLoveList:
            user.removeFromLoveDaily()
            bot.memoryManager.updateUserRecord(user, False)
        bot.memoryManager.pickleMemoryFileToDrive()
    else:
        logg.logSmth(f"##### - {0} users to be un-Loved")

    ### Un Follow ###
    if unfollowList:
        logg.logSmth(f"##### - {len(unfollowList)} users to be un-Followed")

        userNotFound_counter = 0
        for user in unfollowList:
            user.daysSinceYouGotFollowed_Unfollowed('follow', True)

            # logg.logSmth(f"### Navigating to user {user.handle}")
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
            userNotFound_counter = 0  # restart this counter as we only want to see if we fail to get X users in a row, before shuting things down

            if 'OK' in userPage.unfollow():
                user.markDateUnfollowed()
                bot.memoryManager.updateUserRecord(user)
                bot.botSleep()
    else:
        logg.logSmth(f"##### - {0} users to be un-Followed")

    ### Follow Reserves ###
    if reservesList and bot.followMana > 0:
        logg.logSmth(f"##### - {len(reservesList)} reserve users to be Followed")

        userNotFound_counter = 0
        for user in reservesList:
            # logg.logSmth(f"### Navigating to user {user.handle}")
            searchPage = bot.navRibons.goToSearchPage()
            userPage = searchPage.navigateToUserPage(user.handle)

            if not userPage:
                bot.memoryManager.userPageCannotBeFound(user)

                userNotFound_counter += 1
                if userNotFound_counter > 3:
                    return "No Internet - ...or search shadow ban"

                continue

            logg.logSmth(f"########## Will follow user {user.handle}", 'INFO')
            userNotFound_counter = 0  # restart this counter as we only want to see if we fail to get X users in a row, before shuting things down

            if user.iShouldFollowThisUser() and bot.followMana > 0:
                if 'OK' in userPage.follow():
                    user.markTimeFollowed()
                    user.addToLoveDaily()
                    bot.decrementFolowMana(1)

            bot.memoryManager.updateUserRecord(user)
            if user.dateFollowed_byMe:
                bot.botSleep()
    else:
        logg.logSmth(f"##### - {0} reserve users to be Followed")

    ### USERS MANUALLY ADDED
    if manuallyAddedList and bot.followMana > 0:

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
    else:
        logg.logSmth(f"##### - {0} manually added users to be Followed")

    return "OK"


def L1_criteria(userStats, myFollowers):
    # Filter out users with more followers than myself, 0 posts etc.- aka L1
    followerCountLimit = myFollowers

    if userStats['followers'] > (1.05 * followerCountLimit):
        wording = 'Dropping'
    elif userStats['followers'] < 100:
        wording = 'Dropping'
    elif userStats['posts'] < 3:
        wording = 'Dropping'
    else:
        wording = 'Keeping'

    if "Dropping" in wording:
        return False
    else:
        return True
