from random import randint, choice
from time import sleep

from POM import Locators as loc
from POM import Post_ScrolableArea_POM as postScrol
from POM import Screen_POM as screen


class HomePage(screen.Screen):
    def __init__(self, driver):
        super().__init__(driver)
        self.scrollArea = postScrol.Post_ScrolableArea(self.driver)

    def startWatchingStories(self, duration=randint(20, 60)):
        all_visible_stories_but_mine = self.driver.find_elements_by_id(loc.homePage_ID['storiesCommon'])[1:]

        if all_visible_stories_but_mine:
            all_visible_stories_but_mine = [x for x in all_visible_stories_but_mine if "Unseen" in x.tag_name]
            chosen_story = choice(all_visible_stories_but_mine)

            user = chosen_story.tag_name
            user = user.split("'s story")[0]

            print(f"Whatching {user}'s story for {duration} secs")
            chosen_story.click()

            while duration > 0:
                duration -= 1
                sleep(1)

            print(f"Done watching stories")
            self.driver.back()

    def scrollAnd_Like(self, count=10):
        self.scrollAnd_(self.likePosts, count)

    def scrollAnd_(self, func, count=5):
        result = None
        while not result and count > 0:
            result = func()
            count -= 1
            swipesCount = choice([1, 2, 3])
            for i in range(swipesCount):
                self.vSwipe('small')

    def likePosts(self, randomise=True):
        self.scrollArea.scanScreenForPosts()
        for post in self.scrollArea.posts:
            likeSwitch = randint(1, 4)
            if likeSwitch > 1:  # 3/4 = 75% chance I'm gonna hit the like button
                post.likePost()
            else:
                print(f"Nope! No like for {post.postingUser} cause {likeSwitch}")

        return None
