from random import randint, choice
from time import sleep
import AnyBotLog as logg
from POM import Locators as loc
from POM import Post_ScrolableArea_POM as postScrol
from POM import Screen_POM as screen

STORIES_COMMON_KEY = 'storiesCommon'
UNSEEN_TAG = "Unseen"
SWIPE_COUNT_RANGE = [1, 2, 3]
LIKE_RANDOM_MIN = 3
LIKE_RANDOM_MAX = 4


class HomePage(screen.Screen):
    def __init__(self, driver):
        super().__init__(driver)
        self.scroll_area = postScrol.Post_ScrolableArea(self.driver)

    def start_watching_stories(self, duration=None):
        if not duration:
            lower_bound = randint(10, 25)
            upper_bound = randint(45, 55)
            duration = randint(lower_bound, upper_bound)

        all_stories = self.find_elements_by_id(loc.homePage_ID[STORIES_COMMON_KEY])[1:]
        unseen_stories = self.get_unseen_stories(all_stories)

        if unseen_stories:
            chosen_story = choice(unseen_stories)
            username = chosen_story.tag_name.split("'s story")[0]
            logg.logSmth(f"Watching {username}'s story for {duration} seconds", 'INFO')

            chosen_story.click()
            sleep(duration)

            logg.logSmth("Finished watching stories", 'INFO')
            self.driver.back()

    def get_unseen_stories(self, stories):
        return [story for story in stories if UNSEEN_TAG in story.tag_name]

    def scroll_and_like(self, count=10):
        self.scroll_and_execute(self.like_posts, count)

    def scroll_and_execute(self, func, count=5):
        logg.logSmth(f"Starting {func.__name__} with a count of {count}", 'INFO')
        result = None

        while not result and count > 0:
            result = func()
            count -= 1
            for _ in range(choice(SWIPE_COUNT_RANGE)):
                self.vSwipeUp('small')
            self.reactionWait(0.25)

        logg.logSmth(f"Completed {func.__name__} with remaining count of {count}", 'INFO')

    def farm_first_comments(self):
        self.scroll_area.scan_screen_for_posts([1, 1, 0, 1])
        for post in self.scroll_area.posts:
            print(post.get_first_comment_text())

    def like_posts(self, randomise=True):
        self.scroll_area.scan_screen_for_posts()
        if not self.scroll_area.posts:
            return True

        for post in self.scroll_area.posts:
            like_switch = 2 if not randomise else randint(1, randint(LIKE_RANDOM_MIN, LIKE_RANDOM_MAX))
            if like_switch > 1:
                post.likePost()
                post.goBackFromVideo()

        return None
