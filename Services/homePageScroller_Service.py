import AnyBotLog as logg


def homePageScroll(bot, numberOfPosts):
    logg.logSmth(f"#" * 40)
    logg.logSmth(f" " * 10 + "*" * 5 + " The Home " + "*" * 5 + " " * 10)
    logg.logSmth(f"#" * 40)

    homePage = bot.navRibons.goHome()
    homePage.scrollAnd_Like(int(numberOfPosts / 3))

    homePage = bot.navRibons.goHome()
    homePage.startWatchingStories()

    homePage = bot.navRibons.goHome()
    homePage.scrollAnd_Like(int(numberOfPosts / 3))

    homePage = bot.navRibons.goHome()
    homePage.startWatchingStories()

    homePage = bot.navRibons.goHome()
    homePage.scrollAnd_Like(int(numberOfPosts / 3))
