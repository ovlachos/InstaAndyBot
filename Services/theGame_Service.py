def playTheGame(bot, num):
    print(f"Follow Mana: {bot.followMana}")

    ### Read User Memory
    bot.memoryManager.readMemoryFileFromDrive()

    ### Derive Lists
    reservesList = bot.memoryManager.getListOfReserveUsersToFollow()[:num]
    unfollowList = bot.memoryManager.getListOfUsersToUnFollow(bot.daysBeforeIunFollow)[:num]
    unLoveList = bot.memoryManager.getListOfUsersToUnLove(bot.daysBeforeIunLove)

    ### Un Love ###
    if unLoveList:
        print(f"### - {len(unLoveList)} users to be un-Loved")
        for user in unLoveList:
            user.removeFromLoveDaily()
            bot.memoryManager.updateUserRecord(user, False)
        bot.memoryManager.writeMemoryFileToDrive()
    else:
        print(f"### - {0} users to be un-Loved")

    ### Un Follow ###
    if unfollowList:
        print(f"### - {len(unfollowList)} users to be un-Followed")

        userNotFound_counter = 0
        for user in unfollowList:
            user.daysSinceYouGotFollowed_Unfollowed('follow', True)

            searchPage = bot.navRibons.goToSearchPage()
            userPage = searchPage.navigateToUserPage(user.handle)  # TODO

            if not userPage:
                bot.memoryManager.userPageCannotBeFound(user)

                userNotFound_counter += 1
                if userNotFound_counter > 3:
                    return "No Internet - ...or search shadow ban"

                continue

            print(f"Will unfollow user {user.handle}")
            userNotFound_counter = 0  # restart this counter as we only want to see if we fail to get X users in a row, before shuting things down

            if 'OK' in userPage.unfollow():
                user.markDateUnfollowed()
                bot.memoryManager.updateUserRecord(user)
                bot.botSleep()

    else:
        print(f"### - {0} users to be un-Followed")

    ### Follow Reserves ###
    if reservesList and bot.followMana > 0:
        print(f"### - {len(reservesList)} reserve users to be Followed")

        userNotFound_counter = 0
        for user in reservesList:
            searchPage = bot.navRibons.goToSearchPage()
            userPage = searchPage.navigateToUserPage(user.handle)  # TODO

            if not userPage:
                bot.memoryManager.userPageCannotBeFound(user)

                userNotFound_counter += 1
                if userNotFound_counter > 3:
                    return "No Internet - ...or search shadow ban"

                continue

            print(f"Will follow user {user.handle}")
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
        print(f"### - {0} reserve users to be Followed")

    return "OK"
