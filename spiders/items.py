import scrapy

class ImdbItem(scrapy.Item):
    title = scrapy.Field()
    directors = scrapy.Field()
    writers = scrapy.Field()
    stars = scrapy.Field()
    # popularity = scrapy.Field()
    rating = scrapy.Field()
    company = scrapy.Field()
    genre = scrapy.Field()
    runtime = scrapy.Field()
    mpaa = scrapy.Field()
    year = scrapy.Field()

class TheNumbersItem(scrapy.Item):
    title = scrapy.Field()