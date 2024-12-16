from __future__ import annotations

import AnyBotLog as logg
from BotMemory import BotStats


def get_my_profile(bot):
    """Helper to navigate to own profile."""
    return bot.navRibons.goToOwnProfile()


def calculate_stat_differences(bot, current_stats: dict, previous_stats: dict, time_difference: float) -> list:
    """Helper function to compute stat differences."""
    followed = current_stats.get('following', 0) - previous_stats.get('following', 0)
    new_followers = current_stats.get('followers', 0) - previous_stats.get('followers', 0)
    datetime_now = bot.getTimeStampString()
    return [
        datetime_now,
        current_stats.get('posts', 0),
        current_stats.get('followers', 0),
        current_stats.get('following', 0),
        followed,
        new_followers,
        round(time_difference, 2)
    ]


def get_my_stats(bot) -> None:
    """Main function to record statistics of the bot owner."""
    my_profile = get_my_profile(bot)
    if not my_profile or not my_profile.stats:
        logg.logSmth("Failed to retrieve profile stats.")
        return

    current_stats = my_profile.stats
    previous_stats, previous_timestamp = get_previous_stats(bot)

    if previous_stats:
        time_difference = bot.calcTimeDiff(
            bot.getDateTimeFromString(previous_timestamp),
            bot.getDateTimeNow()
        )
        new_row = calculate_stat_differences(current_stats, previous_stats, time_difference)
        BotStats.record_new_point(new_row, 'myStats')
        bot.updateOwnFollowers(current_stats.get('followers', 0))


def get_my_following_list(bot) -> None:
    """Fetch and record the list of accounts followed by the bot user."""
    my_profile = get_my_profile(bot)
    if my_profile and my_profile.get_following_list():
        if my_profile.following:
            BotStats.record_new_point(my_profile.following, 'myFollowing')


def get_my_follower_list(bot, percentage: float) -> None:
    """Fetch and log the list of followers."""
    my_profile = get_my_profile(bot)
    if my_profile and my_profile.get_followers_list(percentage):
        if my_profile.followers:
            logg.logSmth(my_profile.followers)


def get_previous_stats(bot) -> tuple[dict, str] | None:
    """Fetch previously recorded statistics."""
    frame = bot.fileHandler.CSV_getFrameFromCSVfile("myStats")
    if not frame.empty:
        latest = frame.iloc[0].tolist()
        return (
            {'posts': latest[1], 'followers': latest[2], 'following': latest[3]},
            latest[0]
        )
    return None
