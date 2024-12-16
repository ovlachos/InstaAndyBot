import AnyBotLog as logg


def handle_home_page_actions(bot, number_of_posts):
    def scroll_and_watch(number_to_like):
        """Helper function to scroll and watch stories."""
        home_page = bot.navRibons.goHome()
        home_page.scrollAnd_Like(number_to_like)
        home_page = bot.navRibons.goHome()
        home_page.startWatchingStories()

    log_break = "#" * 40
    log_title = " " * 10 + "*" * 5 + " The Home " + "*" * 5 + " " * 10

    logg.logSmth(log_break)
    logg.logSmth(log_title)
    logg.logSmth(log_break)

    posts_per_iteration = int(number_of_posts / 3)
    for _ in range(3):  # Three iterations
        scroll_and_watch(posts_per_iteration)
