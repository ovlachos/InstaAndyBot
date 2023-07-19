import AnyBotLog as logg
from BotMemory import BotStats


def getMyStats(bot):
    myStats = None

    if myProfile := bot.navRibons.goToOwnProfile():
        myStats = myProfile.stats

    prev_Dict, pastTimeStamp = getPreviousStats(bot)
    if prev_Dict and myStats:
        _extracted_from_getMyStats_(myStats, prev_Dict, bot, pastTimeStamp)


# TODO Rename this here and in `getMyStats`
def _extracted_from_getMyStats_(myStats, prev_Dict, bot, pastTimeStamp):
    followed = myStats.get('following') - prev_Dict.get('following')
    newFollowers = myStats.get('followers') - prev_Dict.get('followers')

    datetimeNow = bot.getTimeStampString()
    timeElapsed_ = bot.calcTimeDiff(bot.getDateTimeFromString(pastTimeStamp), bot.getDateTimeNow())
    timeElapsed = round(timeElapsed_, 2)

    newRow = [datetimeNow,
              myStats.get('posts'),
              myStats.get('followers'),
              myStats.get('following'),
              followed,
              newFollowers,
              timeElapsed
              ]

    BotStats.record_new_point(newRow, 'myStats')
    bot.updateOwnFollowers(myStats.get('followers'))


def getMyFollowingList(bot):
    myFollowing = None

    myProfile = bot.navRibons.goToOwnProfile()
    if myProfile:
        myProfile.get_following_list()

    if myProfile.following:
        myFollowing = myProfile.following
        BotStats.record_new_point(myFollowing, 'myFollowing')


def getMyFollowerList(bot, percentage):
    myFollower = None

    myProfile = bot.navRibons.goToOwnProfile()
    if myProfile:
        myProfile.get_followers_list(percentage)

    if myProfile.followers:
        myFollowers = myProfile.followers
        # BotStats.record_new_point(myFollowing, 'myFollowing')
        logg.logSmth(myFollowers)


def getPreviousStats(bot):
    frame = bot.fileHandler.CSV_getFrameFromCSVfile("myStats")
    latest = frame.iloc[0].tolist()

    if len(latest):
        prevDict = {
            'posts': latest[1],
            'followers': latest[2],
            'following': latest[3]
        }
        return prevDict, latest[0]

    return None
