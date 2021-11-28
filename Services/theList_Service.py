import AnyBotLog as logg
from Services import HasTagUsage_Service as hstgu


#### HASHTAGS ####
def foilowOrCollectUsernamesFromHashtagPages(bot, numberOfTags, numberOfPostsPerTag0):
    import random

    logg.logSmth(f"#" * 40)
    logg.logSmth(f" " * 10 + "*" * 5 + " The List " + "*" * 5 + " " * 10)
    logg.logSmth(f"#" * 40)

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

            hashPage.reactionWait()

            verification = hashPage.verifyPageType()
            if not verification:
                return None

            try:
                hashPage.grid.openPostByOrder(i + 1)  # Open post number i+1
                scrollArea = hashPage.grid.scrollablePostArea
                if scrollArea:
                    scrollArea.reactionWait()
                    scrollArea.scanScreenForPosts(level=[0, 0, 0, 1])

                    if scrollArea.posts[0]:

                        post = scrollArea.posts[0]
                        if post.comment:
                            recorder = hstgu.recordTags(post.getFirstCommentText())
                            if recorder:
                                print(recorder)

                    # I need to rescan scrolable area after recording 1st comment cause the DOM is stale by then
                    scrollArea.scanScreenForPosts(level=[1, 1, 0, 0])

                    if scrollArea.posts[0]:  # Do we have even one post on open/initial scan of scrollable area?
                        post = scrollArea.posts[0]

                        if toLike:
                            liked = post.likePost()
                            logg.logSmth(f"#### Like status of post by {post.postingUser} is {liked}")

                        if not post.header:  # Can I navigate to the user's profile? If not lets go back to the grid and open the next post.
                            continue

                        userProf = post.navigateToPostingUserProfile()  # Have I arrived?
                        if not userProf or not userProf.verifyPageType():
                            logg.logSmth(f"#### This is not a user profile")
                            continue

                        userProf.reactionWait()
                        # logg.logSmth(f"User Profile: {userProf.userName}")
                        # TODO is it a good idea to drop mark1 and just start recording/comparing stats in memory?
                        followedFlag = False
                        if L1_criteria(userProf.stats):  # Can/Should I follow this user?
                            if bot.followMana > 0:
                                if 'OK' in userProf.follow():
                                    followedFlag = True
                                    bot.decrementFolowMana(1)
                                    addUserToMemory(bot, userProf, user=userProf.userName, mark1=True, followed=followedFlag)

                                    bot.navRibons.goBack()
                                    bot.navRibons.reactionWait()
                                    bot.navRibons.goBack()

                                    continue  # So that I can skip adding to user memory twice with a false followedFlag

                            addUserToMemory(bot, userProf, user=userProf.userName, mark1=True, followed=followedFlag)
                        else:
                            addUserToMemory(bot, userProf, user=userProf.userName, mark1=False, followed=followedFlag)

                bot.navRibons.goBack()
                bot.navRibons.reactionWait()
                bot.navRibons.goBack()
            except Exception as e:
                logg.logSmth(e)
                logg.logSmth(f"#### This is within the interaction phase for hashtag {hashPage.tag}")
                continue

    # Load memory file
    bot.memoryManager.readMemoryFileFromDriveJSON()

    # Load Target Hashtags list
    hashList = bot.targetHashtags_List

    if hashList:
        random.shuffle(hashList)
        hashList = hashList[:numberOfTags]  # Reduce the amount of tags to be examined
        logg.logSmth(f"Today's hashtags are: {hashList}, with {numberOfPostsPerTag0} posts per tag")

    for hashtag in hashList:

        hasTagPageVerified = None
        hashPage = None
        failCounter = 0
        # Make sure you've navigated to the recents part of a hashTag page
        while not hasTagPageVerified and failCounter < 3:

            searchPage = bot.navRibons.goToSearchPage()
            if not searchPage:
                failCounter += 1
                return 'Fail'

            hashPage = searchPage.navigateToHashTagPage(hashtag)
            if not hashPage:
                bot.navRibons.goHome()
                continue

            hasTagPageVerified = hashPage.verifyPageType(hashtag)
            # logg.logSmth(f"#### Verified {hashtag}: {hasTagPageVerified}")

        # Once at the hashtag page interact with the most recent posts
        # logg.logSmth(f"### At HashTag page for tag: {hashtag}")
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

        logg.logSmth(f"########## User {user} added to memory with mark1={mark1} and followed={followed}")
        logg.logSmth(f"########## Follow mana left: {bot.followMana} || {bot.followManaMax - bot.followMana} users followed today")
    else:
        if not newFollower:
            logg.logSmth(f"########## User {user} NOT added to memory with mark1={mark1} and followed={followed}")
        else:
            logg.logSmth(f"########## User {user} already exists in memory with mark1={mark1} and followed={followed}")

    return "OK"
