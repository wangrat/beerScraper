import re
import urllib

import scrapy
import scrapy_splash

from beerScraper.items import Beer
from googlesearch import search


# this example needs the scrapyjs package: pip install scrapyjs
# it also needs a splash instance running in your env or on Scrapy Cloud (https://github.com/scrapinghub/splash)
class SplashSpider(scrapy.Spider):
    name = 'splash-spider'

    start_requests = ['https://www.ratebeer.com/beer/' + str(id) + '/' for id in range(1, 707996)]

    def start_requests(self):
        for link in start_requests:
            yield scrapy_splash.SplashRequest(link, self.parse,
                                              args={
                                                  # optional; parameters passed to Splash HTTP API
                                                  'wait': 3,

                                                  # 'url' is prefilled from request url
                                                  # 'http_method' is set to 'POST' for POST requests
                                                  # 'body' is set to request body for POST requests
                                              },
                                              # optional
                                              )

    def parse(self, response):
        item = Beer()

        item['name'] = response.xpath(
                "//h1[@id='beerName']/text()").extract_first()

        item['image_url'] = response.css("img[title]")[0]['src']

        item['id'] = re.match(r'beer_[0-9]*', item['image_url'])

        yield item

