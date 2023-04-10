rom
random
import randint, choice  # import random number generation functions
from time import sleep  # import sleep function for pausing program execution
import AnyBotLog as logg  # import logging module

# import classes and functions from POM module
from POM import Locators as loc
from POM import Post_ScrolableArea_POM as postScrol
from POM import Screen_POM as screen


# Define a class to represent the Instagram homepage
class HomePage(screen.Screen):
    def __init__(self, driver):
        super().__init__(driver)
        self.scrollArea = postScrol.Post_ScrolableArea(self.driver)

    # Define a method to start watching Instagram stories
    def startWatchingStories(self, duration=None):
        # If no duration is specified, randomly choose a duration between 10-25 seconds or 45-55 seconds
        if not duration:
            durationLowerBound = randint(10, 25)
            durationUpperBound = randint(45, 55)
            duration = randint(durationLowerBound, durationUpperBound)

        # Get a list of all visible Instagram stories except for the user's own story
        all_visible_stories_but_mine = self.findElementsBy_ID(loc.homePage_ID['storiesCommon'])[1:]

        # If there are visible stories
        if all_visible_stories_but_mine:
            # Filter the list to only include stories that haven't been viewed yet
            all_visible_stories_but_mine = [x for x in all_visible_stories_but_mine if "Unseen" in x.tag_name]
            # Choose a random story from the filtered list
            chosen_story = choice(all_visible_stories_but_mine)

            # Get the username of the user whose story was chosen
            user = chosen_story.tag_name
            user = user.split("'s story")[0]

            # Log that the user is watching the chosen story for the specified duration
            logg.logSmth(f"##### Whatching {user}'s story for {duration} secs", 'INFO')
            # Click on the chosen story to start watching it
            chosen_story.click()

            # Wait for the specified duration
            while duration > 0:
                duration -= 1
                sleep(1)

            # Log that the user is done watching stories and navigate back to the homepage
            logg.logSmth(f"##### Done watching stories", 'INFO')
            self.driver.back()

    # Define a method to scroll through posts on the homepage and like them
    def scrollAnd_Like(self, count=10):
        self.scrollAnd_(self.likePosts, count)

    def scrollAnd_(self, func, count=5):
        # This function scrolls down the page and executes a function repeatedly
        # It takes in a function to execute (func) and the number of times to repeat (count)
        logg.logSmth(f"##### Entering scrollAnd_ {func.__name__} with a count of {count}", 'INFO')

        # Initialize the result to None
        result = None

        # Repeat the execution of the function while the result is not returned and the count is greater than 0
        while not result and count > 0:
            # Execute the function
            result = func()
            count -= 1

            # Swipe up 1-3 times randomly after each function execution
            swipesCount = choice([1, 2, 3])
            for i in range(swipesCount):
                self.vSwipeUp('small')
            self.reactionWait(0.25)

        # Log that the function has finished executing
        logg.logSmth(f"##### Returning from scrollAnd_ {func.__name__} with a count of {count}", 'INFO')

    def farmFirstComments(self):
        # This function scans the screen for posts and prints out the first comment of each post
        self.scrollArea.scanScreenForPosts([1, 1, 0, 1])

        # If there are posts on the screen, execute the following code for each post
        if len(self.scrollArea.posts):
            for post in self.scrollArea.posts:
                # Get the first comment of the post and print it out
                textCom = post.getFirstCommentText()
                print(textCom)

    def likePosts(self, randomise=True):
        # This function scans the screen for posts and likes them randomly
        # It takes in a boolean variable randomise that decides if the function should randomly like posts or not
        self.scrollArea.scanScreenForPosts()

        # If there are posts on the screen, execute the following code for each post
        if len(self.scrollArea.posts):
            for post in self.scrollArea.posts:
                # Decide randomly whether to like the post or not
                likeSwitch = 2
                if randomise:
                    regulator = randint(3, 4)
                    likeSwitch = randint(1, regulator)

                # If likeSwitch is greater than 1, like the post and log the response
                if likeSwitch > 1:  # some random chance I'm gonna hit the like button
                    likeResponse = post.likePost()
                    post.goBackFromVideo()

                    # logg.logSmth(f"Like response for {post.postingUser} is {likeResponse}", 'INFO')

                # Otherwise, do not like the post and log the reason
                else:
                    # logg.logSmth(f"Nope! No like for {post.postingUser} cause {likeSwitch}", 'INFO')
                    pass

            # Return None if there are posts on the screen
            return None

        # Return True if there are no posts on the screen
        return True
