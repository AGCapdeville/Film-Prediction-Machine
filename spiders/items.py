import scrapy

class ImdbItem(scrapy.Item):
    title = scrapy.Field()
    directors = scrapy.Field()
    writers = scrapy.Field()
    # stars = scrapy.Field()
    popularity = scrapy.Field()
    rating = scrapy.Field()
    # length = scrapy.Field()
    genre = scrapy.Field()
    runtime = scrapy.Field()

class TheNumbersItem(scrapy.Item):
    title = scrapy.Field()