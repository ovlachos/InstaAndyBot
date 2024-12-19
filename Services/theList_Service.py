import random
import AnyBotLog as logg

MAX_FAILS = 3  # Maximum retries for navigating to hashtag pages


def logHeader():
    """Logs the header for the process."""
    logg.logSmth("#" * 40)
    logg.logSmth(" " * 10 + "*" * 5 + " The List " + "*" * 5 + " " * 10)
    logg.logSmth("#" * 40)


def L1_criteria(userStats, followerLimit):
    """Filters users based on follower count, posts, and following count."""
    return (
            userStats['followers'] <= 1.05 * followerLimit and
            userStats['followers'] >= 100 and
            userStats['posts'] >= 3 and
            userStats['following'] >= 10
    )


def navigateToUserProfile(bot, post):
    """Navigates to a user's profile from a post."""
    user_profile = post.navigateToPostingUserProfile()
    if user_profile and user_profile.verifyPageType():
        return user_profile
    logg.logSmth("#### This is not a user profile")
    bot.navRibons.goBack()
    return None


def processHashtagPosts(bot, numTags, postsPerHashtag, likePosts, followUsers):
    logHeader()

    if followUsers:
        bot.memoryManager.readStoredMemoryFile()

    hashtagList = bot.targetHashtags_List
    if hashtagList:
        random.shuffle(hashtagList)
        hashtagList = hashtagList[:numTags]
        logg.logSmth(f"Today's hashtags are: {hashtagList}, with {postsPerHashtag} posts per hashtag")

    for hashtag in hashtagList:
        failCounter = 0
        hashPage = None

        while failCounter < MAX_FAILS:
            searchPage = bot.navRibons.goToSearchPage()
            if not searchPage:
                failCounter += 1
                return 'Fail'

            hashPage = searchPage.navigateToHashTagPage(hashtag)
            if hashPage and hashPage.verifyPageType(hashtag):
                break
            bot.navRibons.goHome()
            failCounter += 1

        if failCounter >= MAX_FAILS or not hashPage:
            continue

        hashPage.goToRecentPosts()

        for postIndex in range(postsPerHashtag):
            if hashPage.verifyPageType() is False:
                continue

            hashPage.grid.openPostByOrder(postIndex + 1)
            scrollArea = hashPage.grid.scrollablePostArea
            scrollArea.scanScreenForPosts(level=[1, 1, 1, 0])

            if not scrollArea or len(scrollArea.posts) < 1:
                bot.navRibons.goBack()
                continue

            post = scrollArea.posts[0]
            if likePosts:
                post.likePost()

            userProfile = navigateToUserProfile(bot, post)
            if not userProfile:
                failCounter += 1
                continue

            followed = False
            if L1_criteria(userProfile.stats, bot.ownFollowers) and followUsers and bot.followMana > 0:
                if 'OK' in userProfile.follow():
                    followed = True
                    bot.decrementFolowMana(1)
                    userProfile.MuteAll()

            addUserToMemory(bot, userProfile, user=userProfile.userName, mark1=followed, followed=followed)

            bot.navRibons.goBack()

        if failCounter >= MAX_FAILS:
            break

    return 'OK'
