import AnyBotLog as logg
from POM import Desktop_WebPage as ds_page


def getTagsCount(bot):
    dPage = bot.webPage
    hPage = dPage.visitHashTagPage('#street')
    count = hPage.getPostCount()
    print(count)
