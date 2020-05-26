# -*- coding: utf-8 -*-
import scrapy
from items import ImdbItem
from scrapy.crawler import CrawlerProcess
from scrapy import Request
import logging

# tag we want = td class="titleColumn"
# xpath = //*[@id="main"]/div/span/div/div/div[3]/table/tbody/tr[1]/td[2]/a


# options: 
#   collect more data,
#   class weight (to balance data)
#   try normalizing
#   try to have more features


class ImdbSpider(scrapy.Spider):
    name = 'imdbspider'
    allowed_domains = ['imdb.com'] 
    base_url = ['https://www.imdb.com']
    start_urls = ['https://www.imdb.com/list/ls005750764/']
    custom_settings = {'FEED_FORMAT':'csv','FEED_URI':'IMDB_MOVIES.csv'}


    def parse(self, response):
        for href in response.css("h3.lister-item-header a::attr(href)").getall():
            yield response.follow(url=href, callback=self.parse_movie)
        for nextPage in response.css('a.next-page ::attr(href)').extract():
            yield scrapy.Request(response.urljoin(nextPage))
    

    def parse_movie(self, response): 
        item = ImdbItem()
        item['title'] = [ x.replace('\xa0', '')  for x in response.css(".title_wrapper h1::text").getall()][0]
        item['directors'] = response.xpath('//div[@class="credit_summary_item"]/h4[contains(., "Director")]/following-sibling::a/text()').getall()
        
        writers = response.xpath('//*[@id="title-overview-widget"]/div[2]/div[1]/div[3]/a/text()').getall()
        writers2 = (response.xpath('//div[@class="credit_summary_item"]/h4[contains(., "Writers")]/following-sibling::a/text()').getall())
        if writers != "":
            item['writers'] = writers
        else:
            item['writers'] = writers2

        # item['popularity'] = response.css(".titleReviewBarSubItem span.subText::text")[2].re('([0-9]+)')
        item['rating'] = response.css(".ratingValue span::text").get()
        item['runtime'] = response.css(".txt-block time::text").getall()[0].split(' ')[0]
        item['genre'] = response.xpath('//*[@id="titleStoryLine"]/div[4]/a/text()').getall()

        item['company'] = response.xpath('//div[@class="txt-block"]/h4[contains(., "Production Co")]/following-sibling::a/text()').getall()
        for company in range(len(item['company'])):
            item['company'][company] = item['company'][company].strip()

        item['stars'] = response.xpath('//div[@class="credit_summary_item"]/h4[contains(., "Stars")]/following-sibling::a/text()').getall()
        for star in range(len(item['stars'])):
            item['stars'][star] = item['stars'][star].strip()
            if "See full cast & crew" in item['stars'][star]:
                item['stars'].pop(star)

        item['mpaa'] = response.xpath('//div[@class="subtext"]/text()').get().strip()
                                     # //*[@id="title-overview-widget"]/div[1]/div[2]/div/div[2]/div[2]/div[2]
                                    #  //*[@id="title-overview-widget"]/div[1]/div[2]/div/div[2]/div[2]/div/text()[1]

        item['year'] = response.xpath('//*[@id="titleYear"]/a/text()').get().strip()
  
        return item


#         <div class="txt-block">
#            <h4 class="inline">Production Co:</h4>
#               <a href="/company/co0049348?ref_=cons_tt_dt_co_1"> Touchstone Pictures</a>,<a href="/company/co0076881?ref_=cons_tt_dt_co_2"> Silver Screen Partners III</a>      <span class="see-more inline">
#               <a href="companycredits?ref_=tt_dt_co">See more</a>&nbsp;»
#           </span>
#         </div>
        # FULL PATH: /html/body/div[2]/div/div[2]/div/div[3]/div[11]/div[11]
        
        

open('IMDB_MOVIES.csv', 'w').close()

process = CrawlerProcess() # create instance of CrawlerProcess - This class is the one used by all Scrapy commands
process.crawl(ImdbSpider) # pass this spider class to Scrapy
process.start() # the script will block here until the crawling is finished

""" https://docs.scrapy.org/en/latest/topics/practices.html """