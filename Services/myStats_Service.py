import AnyBotLog as logg
from BotMemory import BotStats


def getMyStats(bot):
    myStats = None

    myProfile = bot.navRibons.goToOwnProfile()
    if myProfile:
        myStats = myProfile.stats

    datetimeNow = bot.getTimeStampString()

    prev_Dict = getPreviousStats(bot)
    if prev_Dict and myStats:
        followed = myStats.get('following') - prev_Dict.get('following')
        newFollowers = myStats.get('followers') - prev_Dict.get('followers')
        newRow = [datetimeNow,
                  myStats.get('posts'),
                  myStats.get('followers'),
                  myStats.get('following'),
                  followed,
                  newFollowers,
                  ]

        BotStats.record_new_point(newRow, 'myStats')


def getPreviousStats(bot):
    frame = bot.fileHandler.CSV_getFrameFromCSVfile("myStats")
    last_row = frame.iloc[-1].tolist()

    if len(last_row):
        prevDict = {
            'posts': last_row[1],
            'followers': last_row[2],
            'following': last_row[3]
        }
        return prevDict

    return None
