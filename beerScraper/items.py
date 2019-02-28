# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Beer(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    images = scrapy.Field()
    image_urls = scrapy.Field()
