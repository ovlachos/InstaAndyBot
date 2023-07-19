from time import sleep

import AnyBotLog as logg
from POM import Locators as loc
from POM import Screen_POM as screen
from POM import UserPage_POM as up


class Post(screen.Screen):
    def __init__(self, driver, postBundle):
        super().__init__(driver)
        self.header = None
        self.pic = None
        self.likeButton = None
        self.likeButtonStatus = None
        self.comment = None
        self.postingUser = None
        self.possiblepostingUser = None
        self.firstComment_txt = ""
        self.canLike = False
        # print(f"Generating a post with:")

        # Unpacking my element objects to keep only the selenium webElement objects
        for elementPack in postBundle:
            # print(f"\t{elementPack[1]}")

            if "header" in elementPack[1]:
                self.updateHeader(elementPack[0])
                continue

            if "comment" in elementPack[1]:
                self.updateComment(elementPack[0])
                if not self.header:
                    self.postingUser = self.possiblepostingUser
                continue

            if "like" in elementPack[1]:
                self.updateLike(elementPack[0])
                self.canLike = True
                continue

            if "pic" in elementPack[1]:
                self.updatePic(elementPack[0])
                self.canLike = True
                continue

        self.updatePostingUser()
        sleep(10)

    def updateHeader(self, element):
        if element:
            self.header = element
            self.updatePostingUser()

    def updatePic(self, element):
        if element:
            self.pic = element

    def updateLike(self, element):
        if element:
            try:
                self.likeButton = element
                self.likeButtonStatus = self.likeButton.tag_name
            except Exception as e:
                logg.logSmth(e)

    def updateComment(self, element):
        if element:
            self.comment = element
            if firstComment := self.findElementBy_XPATH(loc.post_XPATH['firstComment']):
                self.possiblepostingUser = firstComment.tag_name

    def updatePostingUser(self):
        if self.header:
            try:
                self.postingUser = self.header.text.split(' ')[0]
            except Exception as e:
                logg.logSmth("Could not update posting user", 'WARNING')

    def updateLikeButtonStatus(self):
        likes = self.findElementsBy_ID(loc.post_ID['like'])
        if len(likes) < 2:
            self.likeButtonStatus = likes[0].tag_name
        else:
            for likeButton in likes:
                if likeButton.id == self.likeButton.id:
                    self.likeButtonStatus = likeButton.tag_name

    def likePost(self):
        """
        This method likes a post if possible.

        Returns:
            True if the post is successfully liked, None otherwise.
        """
        if self.canLike:
            try:
                if self.likeButton and 'ed' not in self.likeButton.tag_name:
                    self.likeButton.click()
                    self.reactionWait(1)
                    return True

                if self.pic:
                    self.doubleClickOnPic()

                    self.reactionWait(1)
                    return True

            except Exception as e:
                if "DOM" not in e.args[0]:
                    logg.logSmth(f"Could Not like post by {self.postingUser} because {e}", "ERROR")
                return None

        return None

    def doubleClickOnPic(self):
        """
        This method performs a double click on a picture.

        Returns:
            None
        """
        height = self.pic.rect['height']
        startY = self.pic.location['y']
        yPoint = startY + (height / 2)
        self.doubleClickCoordinates(700, int(yPoint))

    def expandComments(self):
        if self.comment:
            try:
                self.comment.click()
                self.reactionWait(2)
                self.driver.back()
                return True
            except Exception:
                return False

    def getFirstCommentText(self):
        if self.expandComments():
            if expandedfirstComment := self.findElementBy_ID(loc.post_ID['commentExpanded']):
                self.firstComment_txt = expandedfirstComment.text

            self.driver.back()

        return self.firstComment_txt

    def navigateToPostingUserProfile(self):
        if self.header:
            self.header.click()
            return up.UserPage(self.driver)

    def goBackFromVideo(self):
        if backButton := self.findElementBy_ID(loc.post_ID['backButton']):
            backButton.click()


class Post_ScrolableArea(screen.Screen):
    def __init__(self, driver):
        super().__init__(driver)
        # logg.logSmth("$$$$ GENERATING SCROLABLE AREA $$$$", "INFO")
        self.allElements = []
        self.posts = None

    def findPostPics(self):
        # For some reason find elements by ID is slow if no elements are present of that ID
        # let us look for pics first and if we get zero, then we look for caroussels as well
        # This way we only pay the 10sec penalty only when there are 0 pics and at least one carousel

        pics = self.findElementsBy_ID(loc.post_ID['pic']) or []

        total = pics

        if len(pics) < 1:
            carousels = self.findElementsBy_ID(loc.post_ID['imageCarousel']) or []
            total = pics + carousels

        return total

    def scanScreenForPosts(self, level=None):
        """In summary, the code scans the screen for different types of elements in a post,
        including headers, pictures, like buttons, and comments, and constructs a list of all elements found.
        It then sorts these elements by their y-coordinate and reconstructs the posts from the sorted list.
        The method takes an optional level parameter that determines which types of elements to scan for."""
        if level is None:
            level = [1, 1, 1, 1]
        # Clear all previous elements to start fresh
        self.allElements.clear()
        if self.posts:
            self.posts.clear()

        # Scan for headers
        if level[0] == 1:
            self.headers = self.findElementsBy_ID(loc.post_ID['postingUser'])
            if self.headers:
                for header in self.headers:
                    self.allElements.append([header, 'header'])

        # Scan for pics
        if level[1] == 1:
            self.pics = self.findPostPics()
            if self.pics:
                for pic in self.pics:
                    self.allElements.append([pic, 'pic'])

        # Scan for like buttons
        if level[2] == 1:
            self.likeButtons = self.findElementsBy_ID(loc.post_ID['like'])
            if self.likeButtons:
                for like in self.likeButtons:
                    # Check that the like button is within the screen bounds
                    if self.screenBoundUpper < like.location['y'] < self.screenBoundLower:
                        self.allElements.append([like, 'like'])

        # Scan for comments
        if level[3] == 1:
            self.comments = self.findElementsBy_ID(loc.post_ID['comment'])
            if self.comments:
                for comment in self.comments:
                    self.allElements.append([comment, 'comment'])

        try:
            # Sort all elements by y-coordinate to reconstruct posts
            self.allElements.sort(key=lambda x: x[0].location['y'])
        except Exception as e:
            # If there's an error, set posts to None
            self.posts = None

        # Reconstruct posts
        self.posts = self.reconstructPosts()

    def reconstructPosts(self):
        """
        This method takes the list of all elements on the screen and separates them into individual post objects.

        Returns:
        - postList (list): a list of post objects

        The reconstructPosts method takes the list of all elements on the screen and separates
        them into individual post objects. First, it initializes an empty list postList to store the post objects.
        Then, it loops through each elementPack in the allElements list. If the elementPack does not contain a comment
        (i.e., it's a header, pic, or like button), it adds the elementPack to the bucket list. If the elementPack does
        contain a comment, it adds the elementPack to the bucket list, creates a new Post object using the bucket list,
        appends the new Post object to the postList, and clears the bucket. Finally, if there are any remaining elements
        in the bucket after the loop, it creates a new Post object using the bucket, appends the new Post object to the
        postList, and clears the bucket. The method returns the postList.
        """
        postList = []
        bucket = []

        for elementPack in self.allElements:
            bucket.append(elementPack)
            if 'comment' in elementPack[1]:
                newPost = Post(self.driver, bucket)
                postList.append(newPost)
                bucket.clear()

        if bucket:
            newPost = Post(self.driver, bucket)
            postList.append(newPost)
            bucket.clear()

        return postList

    def reportOnPosts(self):
        """
        This method reports on the current posts on the screen, printing the posting users for each post.

        Returns:
        - None

        The reportOnPosts method reports on the current posts on the screen by printing the posting users for each post.
        First, it checks if there are any posts in the self.posts list. If there are, it loops through each post in the
        list and prints the posting users for each post using the logg.logSmth method. If there are no posts in the self.posts list,
        it logs a message saying "No posts in view yet" using the logg.logSmth method. The method does not return anything.
        """
        if self.posts:
            for post in self.posts:
                logg.logSmth(f"{post.postingUser} .vs. {post.possiblepostingUser}", 'INFO')
        else:
            logg.logSmth("No posts in view yet", 'WARNING')
