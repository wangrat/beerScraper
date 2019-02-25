# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Beer(scrapy.Item):
    name = scrapy.Field()
    image = scrapy.Field()
    image_url = scrapy.Field()
    id = scrapy.Field()
