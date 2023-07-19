import AnyBotLog as logg


def homePageScroll(bot, numberOfPosts):
    logg.logSmth("#" * 40)
    logg.logSmth(" " * 10 + "*" * 5 + " The Home " + "*" * 5 + " " * 10)
    logg.logSmth("#" * 40)

    homePage = bot.navRibons.goHome()
    homePage.scrollAnd_Like(int(numberOfPosts / 3))

    homePage = _extracted_from_homePageScroll_9(bot, numberOfPosts)
    homePage = _extracted_from_homePageScroll_9(bot, numberOfPosts)


# TODO Rename this here and in `homePageScroll`
def _extracted_from_homePageScroll_9(bot, numberOfPosts):
    homePage = bot.navRibons.goHome()
    homePage.startWatchingStories()

    homePage = bot.navRibons.goHome()
    homePage.scrollAnd_Like(int(numberOfPosts / 3))

    return homePage
