import AnyBotLog as logg
from POM import Desktop_WebPage as ds_page


def getTagsCount(bot):
    for tag in bot.targetHashtags_List:
        dPage = bot.webPage
        hPage = dPage.visitHashTagPage(tag)
        count = hPage.getPostCount()

        if not count:
            return

        print(f"Tag: {tag} || Count: {count}")
