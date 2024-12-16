import AnyBotLog as logg
import random

# Constants
FOLLOWER_LIMIT_MULTIPLIER = 1.05
MIN_FOLLOWER_COUNT = 100
MIN_POST_COUNT = 3
MIN_FOLLOWING_COUNT = 10
MAX_FAULTS = 3


def logHeader():
    """Logs the header for the process."""
    logg.logSmth(f"#" * 40)
    logg.logSmth(f" " * 10 + "*" * 5 + " The List " + "*" * 5 + " " * 10)
    logg.logSmth(f"#" * 40)


def filterUserByCriteria(userStats, followerThreshold):
    """
    Determines whether a user meets the criteria for interaction.
    :param userStats: Dictionary containing user statistics.
    :param followerThreshold: Maximum number of followers allowed.
    :return: True if the user meets the criteria; otherwise, False.
    """
    return (
            userStats['followers'] <= FOLLOWER_LIMIT_MULTIPLIER * followerThreshold
            and userStats['followers'] >= MIN_FOLLOWER_COUNT
            and userStats['posts'] >= MIN_POST_COUNT
            and userStats['following'] >= MIN_FOLLOWING_COUNT
    )


def handleFaults(faults, limit=MAX_FAULTS):
    """Returns True if the fault limit is exceeded."""
    return faults > limit


def actOnPosts(bot, hashPage, postsPerTag, likePosts, followUsers):
    """
    Interact with posts on a platform using specified actions such as liking and following users.

    Act on posts by iterating through the desired number of posts specified by `postsPerTag`. For
    each post, depending on the input flags, the function can like the post and navigate to the
    user's profile to follow them, if certain criteria are met. Faults are handled to ensure
    the function continues operation in case of page-type mismatches, unavailable posts, or
    other unexpected issues during execution.

    :param bot: Instance of a bot that enables navigation, interaction, and tracking actions.
    :type bot: CustomBot
    :param hashPage: Active page object representing a hashtag or collection of posts.
    :type hashPage: Page
    :param postsPerTag: Number of posts to act on under the current hashtag or collection.
    :type postsPerTag: int
    :param likePosts: Flag to indicate whether posts should be liked.
    :type likePosts: bool
    :param followUsers: Flag to indicate whether the function should follow users whose posts are acted upon.
    :type followUsers: bool
    :return: None if a critical issue halts execution; otherwise, the function returns implicitly.
    :rtype: None
    """
    faults = 0
    for postOrder in range(postsPerTag):
        if handleFaults(faults):
            return None

        # Verify page type and open the corresponding post
        if not hashPage.verifyPageType():
            faults += 1
            continue
        hashPage.grid.openPostByOrder(postOrder)

        scrollArea = hashPage.grid.scrollablePostArea
        if not scrollArea:  # Check if posts are available
            bot.navRibons.goBack()
            faults += 1
            continue

        post = getFirstPostOnScreen(scrollArea)
        if not post:
            bot.navRibons.goBack()
            faults += 1
            continue

        # Like post if required
        if likePosts:
            post.likePost()

        # Navigate to the user's profile and follow if criteria are met
        userProfile = post.navigateToPostingUserProfile()
        if not userProfile or not userProfile.verifyPageType():
            logg.logSmth(f"#### Invalid user profile")
            bot.navRibons.goBack()
            continue

        if followUsers and bot.followMana > 0 and filterUserByCriteria(userProfile.stats, bot.ownFollowers):
            if 'OK' in userProfile.follow():
                bot.decrementFolowMana(1)
                userProfile.MuteAll()  # Mute user content
                addUserToMemory(bot, userProfile, user=userProfile.userName, mark1=True, followed=True)
        bot.navRibons.goBack()


def followOrCollectUsernamesFromHashtagPages(bot, numberOfTags, postsPerTag, toLike, toFollow):
    """
    Executes actions on recent posts from specified hashtags. The function selects a given
    number of tags from the list of target hashtags and navigates them to execute interactions
    on a specified number of posts per each tag, based on the provided options of liking or
    following.

    :param bot: Instance of the bot responsible for handling navigation, interaction, and
        memory management.
    :type bot: Bot
    :param numberOfTags: The number of hashtags to process in a given execution. Determines
        how many hashtags are randomly selected from the target list.
    :type numberOfTags: int
    :param postsPerTag: The number of posts to process for each hashtag. Determines how many
        recent posts will be acted upon under each hashtag.
    :type postsPerTag: int
    :param toLike: Flag indicating if the bot should like posts while processing. If True,
        it will interact with posts by liking them.
    :type toLike: bool
    :param toFollow: Flag indicating if the bot should follow users while processing. If True,
        it will interact with the users by following them.
    :type toFollow: bool
    :return: A string indicating the status of the operation. Returns 'OK' if hashtags and
        posts were processed successfully; otherwise, returns 'Fail' in cases of repeated
        navigation or processing failures.
    :rtype: str
    """
    logHeader()

    if toFollow:
        bot.memoryManager.readStoredMemoryFile()

    hashtags = bot.targetHashtags_List
    if hashtags:
        random.shuffle(hashtags)
        hashtags = hashtags[:numberOfTags]
        logg.logSmth(f"Today's hashtags are: {hashtags}, with {postsPerTag} posts per tag")

    for hashtag in hashtags:
        hashPage = None
        faults = 0
        while not (hashPage and hashPage.verifyPageType(hashtag)) and faults < MAX_FAULTS:
            searchPage = bot.navRibons.goToSearchPage()
            if not searchPage:
                faults += 1
                return 'Fail'
            hashPage = searchPage.navigateToHashTagPage(hashtag)
            if not hashPage:
                bot.navRibons.goHome()
                faults += 1

        if hashPage:
            hashPage.goToRecentPosts()
            actOnPosts(bot, hashPage, postsPerTag, toLike, toFollow)

    return 'OK'


def getFirstPostOnScreen(scrollArea):
    """
    Retrieves the first post in the visible area of the scrollable post area.
    """
    scrollArea.scanScreenForPosts(level=[1, 1, 0, 0])
    return scrollArea.posts[0] if scrollArea.posts else None


def addUserToMemory(bot, userPage, user, mark1=False, followed=False):
    """
    Adds the user to the bot's memory.
    """
    bot.memoryManager.addUser(user, mark1=mark1, followed=followed)
