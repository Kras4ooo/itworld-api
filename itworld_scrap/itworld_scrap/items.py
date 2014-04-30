from scrapy.item import Item, Field

class ItworldScrapItem(Item):
    title = Field()
    author = Field()
    content = Field()
    post_date = Field()