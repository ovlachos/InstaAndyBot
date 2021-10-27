from random import randint, choice
from time import sleep
import AnyBotLog as logg

from POM import Locators as loc
from POM import Post_ScrolableArea_POM as postScrol
from POM import Screen_POM as screen


class HomePage(screen.Screen):
    def __init__(self, driver):
        super().__init__(driver)
        self.scrollArea = postScrol.Post_ScrolableArea(self.driver)

    def startWatchingStories(self, duration=None):
        if not duration:
            durationLowerBound = randint(10, 25)
            durationUpperBound = randint(45, 55)
            duration = randint(durationLowerBound, durationUpperBound)

        all_visible_stories_but_mine = self.driver.find_elements_by_id(loc.homePage_ID['storiesCommon'])[1:]

        if all_visible_stories_but_mine:
            all_visible_stories_but_mine = [x for x in all_visible_stories_but_mine if "Unseen" in x.tag_name]
            chosen_story = choice(all_visible_stories_but_mine)

            user = chosen_story.tag_name
            user = user.split("'s story")[0]

            logg.logSmth(f"##### Whatching {user}'s story for {duration} secs", 'INFO')
            chosen_story.click()

            while duration > 0:
                duration -= 1
                sleep(1)

            logg.logSmth(f"##### Done watching stories", 'INFO')
            self.driver.back()

    def scrollAnd_Like(self, count=10):
        self.scrollAnd_(self.likePosts, count)

    def scrollAnd_(self, func, count=5):
        logg.logSmth(f"##### Entering scrollAnd_ {func.__name__} with a count of {count}", 'INFO')

        result = None
        while not result and count > 0:
            result = func()
            count -= 1
            swipesCount = choice([1, 2, 3])
            for i in range(swipesCount):
                self.vSwipe('small')
            self.reactionWait(0.5)

        logg.logSmth(f"##### Returning from scrollAnd_ {func.__name__} with a count of {count}", 'INFO')

    def likePosts(self, randomise=True):
        self.scrollArea.scanScreenForPosts()

        if len(self.scrollArea.posts):
            for post in self.scrollArea.posts:

                likeSwitch = 2
                if randomise:
                    regulator = randint(3, 6)
                    likeSwitch = randint(1, regulator)

                if likeSwitch > 1:  # some random chance I'm gonna hit the like button
                    likeResponse = post.likePost()
                    # logg.logSmth(f"Like response for {post.postingUser} is {likeResponse}", 'INFO')
                else:
                    # logg.logSmth(f"Nope! No like for {post.postingUser} cause {likeSwitch}", 'INFO')
                    pass

            return None

        return True
