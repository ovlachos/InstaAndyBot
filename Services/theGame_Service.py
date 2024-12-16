import AnyBotLog as logg
from BotMemory import InfidelsList

# Constants
HEADER_DIVIDER = "#" * 40
HEADER_TITLE = " " * 10 + "*" * 5 + " The Game " + "*" * 5 + " " * 10
USER_NOT_FOUND_THRESHOLD = 3


def log_header():
    """Logs a standardized header for the game."""
    logg.logSmth(HEADER_DIVIDER)
    logg.logSmth(HEADER_TITLE)
    logg.logSmth(HEADER_DIVIDER)


def navigate_to_user_page(bot, user_handle):
    """
    Navigate to a user's page using the given bot and user handle.

    This function interacts with a bot to navigate to the search page. If the
    navigation to the search page fails, it attempts to go back and try again.
    Once on the search page, it navigates to the specified user's page.

    :param bot: The bot object responsible for navigation and search operations.
    :type bot: object
    :param user_handle: The unique handle of the user to navigate to.
    :type user_handle: str
    :return: The result of the user page navigation, typically a page object or success indicator.
    :rtype: object
    """
    search_page = None
    while not search_page:
        search_page = bot.navRibons.goToSearchPage()
        if not search_page:
            bot.navRibons.goBack()
    return search_page.navigateToUserPage(user_handle)


def process_unfollow(bot, user_list, category_name):
    """
    Process the unfollowing of users in a specified category.

    This function takes a bot instance, a list of users, and a category name, then attempts to
    unfollow users in the provided list. It handles scenarios where a user's page cannot be found,
    manages error counters, updates user records, and logs the progress of the unfollowing
    process. If a threshold for unfound user pages is reached, the operation stops and returns
    a specified status.

    :param bot: The bot instance used to interact with user pages and handle operations like
        navigation, unfollowing, memory management, and logging.
    :type bot: Bot
    :param user_list: A list of users to process for unfollowing. Each user is expected to have
        methods and attributes such as `handle` and `markDateUnfollowed`.
    :type user_list: list[User]
    :param category_name: The name of the category to which the users belong. This is used for
        logging purposes.
    :type category_name: str
    :return: A string indicating the status or result of the operation. Possible values include
        a success indicator or an error/state message when a threshold is reached.
    :rtype: str
    """
    if user_list:
        logg.logSmth(f"##### - {len(user_list)} {category_name} users to be unfollowed")
        user_not_found_counter = 0
        unfollow_counter = 0

        for user in user_list:
            user_page = navigate_to_user_page(bot, user.handle)
            if not user_page:
                # User page not found; increment error counter
                bot.memoryManager.userPageCannotBeFound(user)
                user_not_found_counter += 1
                if user_not_found_counter > USER_NOT_FOUND_THRESHOLD:
                    return "No Internet - ...or search shadow ban"
                continue

            logg.logSmth(f"########## Will unfollow user {user.handle}")
            user_not_found_counter = 0  # Reset counter on success
            if 'OK' in user_page.unfollow():
                user.markDateUnfollowed()
                bot.memoryManager.updateUserRecord(user)
                unfollow_counter += 1
                logg.logSmth(f"##### {unfollow_counter} / {len(user_list)} users unfollowed today")
                bot.botSleep()
    else:
        logg.logSmth(f"##### - No {category_name} users to be unfollowed")


def playTheGame(bot, num):
    """
    Executes the core gameplay logic for the bot. This involves reading and updating
    bot memory, processing unfollows and purges, as well as inspecting and following
    manually added users.

    :param bot: The bot instance responsible for managing social media user interactions.
    :type bot: Bot
    :param num: The number of users to process in the derived operation lists.
    :type num: int
    :return: Returns a string indicating the status of the operation, such as "OK"
        on success or a descriptive error message.
    :rtype: str
    """
    # Log header
    log_header()

    # Read bot memory
    bot.memoryManager.readStoredMemoryFile()

    # Update bot stats
    bot.myStats_Service()

    # Derive user lists
    unfollow_list = bot.memoryManager.getListOfUsersToUnFollow(bot.daysBeforeIunFollow)  # [:num]
    purge_list = InfidelsList.infidels
    manually_added_list = bot.memoryManager.manuallyAddNewUsersTo_theGame()

    # Process unfollowing users
    process_unfollow(bot, unfollow_list, "unfollow")
    process_unfollow(bot, purge_list, "purge")

    # Manually added users to follow
    if manually_added_list and bot.followMana > 0:
        manually_added_list = manually_added_list[:bot.followMana]
        logg.logSmth(f"##### - {len(manually_added_list)} manually added users to be inspected/followed")
        user_not_found_counter = 0

        for user in manually_added_list:
            logg.logSmth(f"########## Navigating to user {user.handle}")
            user_page = navigate_to_user_page(bot, user.handle)

            if not user_page:
                bot.memoryManager.userPageCannotBeFound(user)
                user_not_found_counter += 1
                if user_not_found_counter > USER_NOT_FOUND_THRESHOLD:
                    return "No Internet - ...or search shadow ban"
                continue

            user_not_found_counter = 0  # Reset counter
            user.addToL1()  # Add to L1 list
            if user.iShouldFollowThisUser() and bot.followMana > 0:
                logg.logSmth(f"########## Will follow user {user.handle}", 'INFO')
                if 'OK' in user_page.follow():
                    user.markTimeFollowed()
                    user.addToLoveDaily()
                    bot.decrementFolowMana(1)
            else:
                logg.logSmth(f"########## Manually added user {user.handle} not worthy", 'INFO')

            bot.memoryManager.updateUserRecord(user)
            if user.dateFollowed_byMe:
                bot.botSleep()
    else:
        logg.logSmth("##### - No manually added users to be inspected/followed")

    return "OK"


def L1_criteria(userStats, myFollowers):
    """
    Filters and evaluates user statistics to determine whether to include or exclude a user. The filtering logic
    is based on evaluating the number of followers a user has in comparison to the follower threshold,
    and the conditions of having minimum posts and followers. Users not meeting the criteria are excluded.

    :param userStats: A dictionary containing user statistics such as 'followers' (int) and 'posts' (int).
    :param myFollowers: Integer representing the number of followers for the current account.
    :return: A boolean value. Returns True if the user meets the specified inclusion criteria, otherwise False.
    """
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
