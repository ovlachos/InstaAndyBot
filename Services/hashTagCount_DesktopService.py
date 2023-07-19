import AnyBotLog as logg
from POM import Desktop_WebPage as ds_page


def getTagsCount(bot):
    for tag in bot.targetHashtags_List:
        dPage = bot.webPage
        hPage = dPage.visitHashTagPage(tag)
        if count := hPage.getPostCount():
            print(f"Tag: {tag} || Count: {count}")
        else:
            return
