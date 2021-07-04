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
        self.liked = False
        self.canLike = False
        self.count = 0

        # Unpacking my element objects to keep only the selenium webElement objects
        for elementPack in postBundle:
            if "header" in elementPack[1]:
                self.updateHeader(elementPack[0])
                self.count += 1
                continue

            if "pic" in elementPack[1]:
                self.updatePic(elementPack[0])
                self.canLike = True
                self.count += 1
                continue

            if "like" in elementPack[1]:
                self.updateLike(elementPack[0])
                self.canLike = True
                self.count += 1
                continue

            if "comment" in elementPack[1]:
                self.updateComment(elementPack[0])
                self.count += 1
                if not self.header:
                    self.postingUser = self.possiblepostingUser
                continue

        self.updatePostingUser()

    def updateHeader(self, element):
        if element:
            self.header = element
            self.updatePostingUser()

    def updatePic(self, element):
        if element:
            self.pic = element

    def updateLike(self, element):
        if element:
            self.likeButton = element
            self.likeButtonStatus = self.likeButton.tag_name

    def updateComment(self, element):
        if element:
            self.comment = element
            firstComment = self.findElementBy_XPATH(loc.post_XPATH['firstComment'])
            if firstComment:
                self.possiblepostingUser = firstComment.tag_name

    def updateLikeButtonStatus(self):
        likes = self.findElementsBy_ID(loc.post_ID['like'])
        if len(likes) < 2:
            self.likeButtonStatus = likes[0].tag_name
        else:
            for likeButton in likes:
                if likeButton.id == self.likeButton.id:
                    self.likeButtonStatus = likeButton.tag_name

    def likePost(self):

        if self.canLike and not self.liked:
            try:
                print(f'Intent is to like post from {self.postingUser}')

                if self.pic and not self.liked:
                    # print(f"Pic y= {self.pic.location['y']}")
                    self.doubleClick(self.pic)
                    self.reactionWait(1)
                    self.liked = True
                    return True

                if self.likeButton and not self.liked:

                    if 'ed' not in self.likeButton.tag_name:
                        # print(f"Like y= {self.likeButton.location['y']}")
                        self.likeButton.click()
                        self.reactionWait(1)
                        self.liked = True
                        return True

            except Exception as e:
                print(f"Could Not like post by {self.postingUser} because {e}")
                return None

        return None

    def updatePostingUser(self):
        if self.header:
            self.postingUser = self.header.text.split(' ')[0]

    def navigateToPostingUserProfile(self):
        if self.header:
            self.header.click()
            return up.UserPage(self.driver)


class Post_ScrolableArea(screen.Screen):
    def __init__(self, driver):
        super().__init__(driver)
        self.allElements = []
        self.posts = None
        self.scanScreenForPosts()

    def findPostPics(self):
        # For some reason find elements by ID is slow if no elements are present of that ID
        # let us look for pics first and if we get zero, then we look for caroussels as well
        # This way we only pay the 10sec penalty only when there are 0 pics and at least one carousel

        pics, carousels = [], []
        pics = self.findElementsBy_ID(loc.post_ID['pic'])
        total = pics

        if len(pics) < 1:
            carousels = self.findElementsBy_ID(loc.post_ID['imageCarousel'])
            total = pics + carousels

        return total

    def scanScreenForPosts(self):

        self.allElements.clear()
        if self.posts:
            self.posts.clear()

        self.headers = self.findElementsBy_ID(loc.post_ID['postingUser'])
        for header in self.headers:
            self.allElements.append([header, 'header'])

        self.pics = self.findPostPics()
        for pic in self.pics:
            if self.screenBoundUpper < pic.location['y'] < self.screenBoundLower:  # TODO: Find a more versatile limit
                self.allElements.append([pic, 'pic'])
            # else:
            #     print(f"Image out of bounds. y = {pic.location['y']}")

        self.likeButtons = self.findElementsBy_ID(loc.post_ID['like'])
        for like in self.likeButtons:
            if self.screenBoundUpper < like.location['y'] < self.screenBoundLower:  # TODO: Find a more versatile limit
                self.allElements.append([like, 'like'])
            # else:
            #     print(f"Like out of bounds. y = {like.location['y']}")

        self.comments = self.findElementsBy_ID(loc.post_ID['comment'])
        for comment in self.comments:
            self.allElements.append([comment, 'comment'])

        self.allElements.sort(key=lambda x: x[0].location['y'])
        self.posts = self.reconstructPosts()

    def reconstructPosts(self):
        postList = []
        bucket = []
        for elementPack in self.allElements:
            if 'comment' not in elementPack[1]:
                bucket.append(elementPack)
            else:
                bucket.append(elementPack)
                newPost = Post(self.driver, bucket)
                postList.append(newPost)
                bucket.clear()

        if len(bucket) > 0:
            newPost = Post(self.driver, bucket)
            postList.append(newPost)
            bucket.clear()

        return postList

    def reportOnPosts(self):
        if self.posts:
            for post in self.posts:
                print(f"{post.postingUser} .vs. {post.possiblepostingUser}")
                print(post.count)
        else:
            print("No posts in view yet")
