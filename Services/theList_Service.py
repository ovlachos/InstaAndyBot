import AnyBotLog as logg


# ~~~ HASHTAGS ~~~#
def followOrCollectUsernamesFromHashtagPages(bot, numberOfTags, numberOfPostsPerTag0, toLike, toFollow):
    import random

    # Start logging with a header
    logg.logSmth(f"#" * 40)
    logg.logSmth(f" " * 10 + "*" * 5 + " The List " + "*" * 5 + " " * 10)
    logg.logSmth(f"#" * 40)

    # L1 criteria function, used for filtering out unwanted users
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

    def actOnPostingUsers(toLike_, toFollow_):
        """
        Like and/or follow the posting users of the hashtag currently navigated by the bot.

        :param toLike_: A boolean indicating whether to like the post of each posting user or not.
        :param toFollow_: A boolean indicating whether to follow the posting user or not.
        :return: None if the page type verification fails, otherwise nothing.
        """
        # Initialize variables
        number_of_faults = 0

        # Iterate over the number of posts per tag
        for i in range(0, numberOfPostsPerTag):

            # Wait for a random time within the range of reaction interval
            hashPage.reactionWait()

            # Verify that the current page is a valid page type
            verification = hashPage.verifyPageType()
            if not verification:
                return None

            # Open the i-th post on the grid
            hashPage.grid.openPostByOrder(i + 1)

            # Get the scrollable post area
            scroll_area = hashPage.grid.scrollablePostArea

            # Check if there is at least one post on the current screen
            if not scroll_area or not scroll_area.posts[0]:
                # If not, return to the grid and move on to the next post
                bot.navRibons.goBack()
                continue

            # Get the first post on the current screen
            post = scroll_area.posts[0]

            # Like the post if toLike is True
            if toLike_:
                liked = post.likePost()
                # logg.logSmth(f"#### Like status of post by {post.postingUser} is {liked}")

            # Navigate to the posting user's profile
            user_prof = post.navigateToPostingUserProfile()

            # Check if the navigation was successful
            if not user_prof or not user_prof.verifyPageType():
                logg.logSmth(f"#### This is not a user profile")
                bot.navRibons.goBack()
                continue

            # Wait for a random time within the range of reaction interval
            user_prof.reactionWait()

            # Check if the bot should follow the user based on L1 criteria
            followed_flag = False
            if L1_criteria(user_prof.stats) and toFollow_ and bot.followMana > 0:
                # Follow the user
                if 'OK' in user_prof.follow():
                    followed_flag = True
                    bot.decrementFolowMana(1)
                    # Mute user's stories and posts
                    user_prof.MuteAll()

            # Add the posting user to memory with appropriate flags
            addUserToMemory(bot, user_prof, user=user_prof.userName, mark1=followed_flag, followed=followed_flag)

            # Return to the grid
            bot.navRibons.goBack()

            # Wait for a random time within the range of reaction interval
            bot.navRibons.reactionWait()

            # Return to the hashtag page
            bot.navRibons.goBack()

            # Check if there are too many faults
            if number_of_faults > 3:
                return
            else:
                number_of_faults += 1

    # Load memory file
    if toFollow:
        bot.memoryManager.readStoredMemoryFile()

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
        # Make sure you've navigated to the recent part of a hashTag page
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

        # Once at the hashtag page interact with the most recent posts
        # logg.logSmth(f"### At HashTag page for tag: {hashtag}")
        numberOfPostsPerTag = numberOfPostsPerTag0

        # Collect user handles OR Follow Users
        hashPage.goToRecentPosts()  # Go to most recent posts grid
        actOnPostingUsers(toLike, toFollow)

    return 'OK'


def getFirstPostOnScreen(scrollArea):
    """
    Retrieves the first post in the visible area of the scrollable post area.

    :param scrollArea: A ScrollablePostArea instance.
    :return: The first Post instance on the visible area of the scrollable post area, or None if no posts are found.
    """

    scrollArea.scanScreenForPosts(level=[1, 1, 0, 0])

    if scrollArea.posts:
        return scrollArea.posts[0]

    return None


def addUserToMemory(bot, userPage, user, mark1=False, followed=False):
    # Add user to bot's memory manager
    bot.memoryManager.addUserToMemory(user)

    # Get the newly created memory object of the new user
    new_follower = bot.memoryManager.retrieveUserFromMemory(user)

    # Check if user is new to the system and update memory accordingly
    if new_follower and not new_follower.thisUserHasBeenThroughTheSystem():
        # Add user to level 0 and level 2 lists
        new_follower.addToL0('hashtag')
        new_follower.addToL2()

        # Update user's information from live Instagram page
        new_follower.updateInfoFromLivePage_Landing(userPage)

        # Add user to level 1 list if mark1 flag is True
        if mark1:
            new_follower.addToL1()

        # Mark user as followed and add to love daily list if followed flag is True
        if followed:
            new_follower.markTimeFollowed()
            new_follower.addToLoveDaily()

        # Update user record in memory manager
        bot.memoryManager.updateUserRecord(new_follower)

        # Uncomment the following lines to log information
        # logg.logSmth(f"########## User {user} added to memory with mark1={mark1} and followed={followed} || F/f/P = {follower_count}/{following_count}/{post_count}")
        # logg.logSmth(f"########## Follow mana left: {bot.followMana} || {bot.followManaMax - bot.followMana} users followed today")
    else:
        if not new_follower:
            pass
            # Uncomment the following line to log information
            # logg.logSmth(f"########## User {user} NOT added to memory with mark1={mark1} and followed={followed} || F/f/P = {follower_count}/{following_count}/{post_count}")
        else:
            pass
            # Uncomment the following line to log information
            # logg.logSmth(f"########## User {user} already exists in memory with mark1={mark1} and followed={followed} || F/f/P = {follower_count}/{following_count}/{post_count}")
    return "OK"
