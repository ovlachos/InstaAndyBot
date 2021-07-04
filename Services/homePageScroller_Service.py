def homePageScroll(bot, numberOfPosts):
    homePage = bot.navRibons.goHome()
    homePage.scrollAnd_Like(int(numberOfPosts / 2))

    homePage = bot.navRibons.goHome()
    homePage.startWatchingStories()

    homePage = bot.navRibons.goHome()
    homePage.scrollAnd_Like(int(numberOfPosts / 2))

    homePage = bot.navRibons.goHome()
    homePage.startWatchingStories()
