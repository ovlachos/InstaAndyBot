#### HASHTAGS ####

def foilowOrCollectUsernamesFromHashtagPages(bot, numberOfTags, numberOfPostsPerTag0):
    import random

    def L1_criteria(userStats):
        # Filter out users with more followers than myself, 0 posts etc.- aka L1
        followerCountLimit = bot.ownFollowers

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

    def actOnPostingUsers(toLike=True):

        for i in range(0, numberOfPostsPerTag):
            try:
                hashPage.reactionWait()

                hashPage.grid.openPostByOrder(i + 1)  # Open post number i+1
                scrollArea = hashPage.grid.scrollablePostArea
                if scrollArea:
                    scrollArea.reactionWait()

                    if scrollArea.posts[0]:  # Do we have even one post on open/initial scan of scrollable area?
                        post = scrollArea.posts[0]

                        if toLike:
                            liked = post.likePost()

                        if not post.header:  # Can I navigate to the user's profile?
                            continue

                        userProf = post.navigateToPostingUserProfile()  # Have I arrived?
                        if not userProf:
                            continue

                        userProf.reactionWait()

                        followedFlag = False
                        if L1_criteria(userProf.stats):  # Can/Should I follow this user?
                            if bot.followMana > 0:
                                if 'OK' in userProf.follow():
                                    followedFlag = True
                                    bot.decrementFolowMana(1)
                                    addUserToMemory(bot, userProf, user=userProf.userName, mark1=True, followed=followedFlag)

                                    bot.navRibons.goBack()
                                    bot.navRibons.reactionWait(0.5)
                                    bot.navRibons.goBack()

                                    continue  # So that I can skip adding to user memory twice with a false followedFlag

                            addUserToMemory(bot, userProf, user=userProf.userName, mark1=True, followed=followedFlag)
                        else:
                            addUserToMemory(bot, userProf, user=userProf.userName, mark1=False, followed=followedFlag)

                bot.navRibons.goBack()
                bot.navRibons.reactionWait(0.5)
                bot.navRibons.goBack()
            except Exception as e:
                print(e)
                continue

    # Load memory file
    bot.memoryManager.readMemoryFileFromDrive()

    # Load Target Hashtags list
    hashList = bot.targetHashtags_List

    if hashList:
        random.shuffle(hashList)
        hashList = hashList[:numberOfTags]  # Reduce the amount of tags to be examined
        print(f"Today's hashtags are: {hashList}, with {numberOfPostsPerTag0} posts per tag")

    for hashtag in hashList:
        hashPage = None
        while not hashPage:
            searchPage = bot.navRibons.goToSearchPage()
            hashPage = searchPage.naviateToHashTagPage(hashtag)

        print(f"### HashTag: {hashtag}")
        numberOfPostsPerTag = numberOfPostsPerTag0

        # Collect user handles OR Follow Users
        hashPage.goToRecentPosts()  # Go to most recent posts grid
        actOnPostingUsers()

    return 'OK'


def addUserToMemory(bot, userPage, user, mark1=False, followed=False):
    bot.memoryManager.addUserToMemory(user)

    # Get the newly created memory object of the new user
    newFollower = bot.memoryManager.retrieveUserFromMemory(user)
    if newFollower and not newFollower.thisUserHasBeenThroughTheSystem():
        newFollower.addToL0('hashtag')
        newFollower.addToL2()

        newFollower.updateInfoFromLivePage_Landing(userPage)

        if mark1:
            newFollower.addToL1()

        if followed:
            newFollower.markTimeFollowed()
            newFollower.addToLoveDaily()

        bot.memoryManager.updateUserRecord(newFollower)

        print(f"##### User {user} added to memory with mark1={mark1} and followed={followed}")
    else:
        print(f"##### User {user} NOT added to memory with mark1={mark1} and followed={followed}")

    return "OK"
