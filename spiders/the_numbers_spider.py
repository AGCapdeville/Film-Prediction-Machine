# -*- coding: utf-8 -*-
import scrapy
from items import TheNumbersItem
from scrapy.crawler import CrawlerProcess
from scrapy import Request

# tag we want = td class="titleColumn"

# xpath = //*[@id="main"]/div/span/div/div/div[3]/table/tbody/tr[1]/td[2]/a


class The_Number_spider(scrapy.Spider):
    name = 'the_number_spider'  # eg name to use when running the script
    # Let’s say your target url is https://www.example.com/1.html, then add 'example.com' to the list.
    allowed_domains = ['the-numbers.com']
    base_url = ['https://www.the-numbers.com/']
    start_urls = ['https://www.the-numbers.com/movie/budgets/all']
    # add this to save file as csv #
    custom_settings = {'FEED_FORMAT': 'csv',
                       'FEED_URI': 'THE_NUMBERS_MOVIES.csv'}
                
    def start_requests(self):
        headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield Request(url, headers=headers)

    def parse(self, response):
        print("the response:", response)
        print("=" * 100)
        start_tail = ['https://www.the-numbers.com/movie/budgets/all']
        rows_in_big_table = response.xpath("//table/tr")

        for i, onerow in enumerate(rows_in_big_table):
            if i != 0:
                print("\nwhat are you =", onerow)
                print("done\n")
                movie_item = TheNumbersItem()
                movie_title = onerow.xpath('td/b/a/text()').extract()[0]
                movie_item['title'] = movie_title
                print("we did it")
                yield movie_item
        headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for nextPage in range(101, 6001, 100):
            next_url = start_tail[0] + '/' + str(nextPage)
            print("=" * 100)
            print("next_url:", next_url)
            print("=" * 100)
            yield Request(next_url, headers=headers)

# Add this to run everything from this script - just use "sudo python3 imdbSpider"
# create instance of CrawlerProcess - This class is the one used by all Scrapy commands
process=CrawlerProcess()
process.crawl(The_Number_spider)  # pass this spider class to Scrapy
process.start()  # the script will block here until the crawling is finished

""" https://docs.scrapy.org/en/latest/topics/practices.html """
