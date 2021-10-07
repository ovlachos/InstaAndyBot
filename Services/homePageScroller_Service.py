def homePageScroll(bot, numberOfPosts):
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
