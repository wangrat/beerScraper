import json
import re

import scrapy
import scrapy_splash

from beerScraper.items import Beer


# this example needs the scrapyjs package: pip install scrapyjs
# it also needs a splash instance running in your env or on Scrapy Cloud (https://github.com/scrapinghub/splash)
class SplashSpider(scrapy.Spider):
    name = 'splash-spider'

    start_url = 'http://www.ratebeer.com/beer/'

    lua_script = open('splash.lua', 'r').read()

    file = open('beers.json', 'r')

    beers = json.load(file)

    file.close()

    ids_seen = [beer['id'] for beer in beers['beers']]

    ids_seen = set(ids_seen)

    def start_requests(self):
        for beerId in list(filter(lambda x: x not in self.ids_seen, range(200, 300))):
            yield scrapy_splash.SplashRequest(self.start_url + str(beerId) + '/', self.parse,
                                              args={
                                                  'lua_source': self.lua_script
                                              },
                                              meta={'id': beerId}
                                              )

    def parse(self, response):
        item = Beer()

        item['name'] = str(response.xpath("//h1[@id='beerName']/text()").get())

        item['image_urls'] = [str(response.css("#toggleImage > img::attr(src)").get())]

        item['id'] = response.meta['id']

        item['deleted'] = response.css("h2 > span").get() is not None

        item['alias'] = response.xpath("//*[@id='root']/div/div[2]/div/div[1]/div/div[2]/span").get() is not None

        if item['deleted'] or item['alias']:
            item['image_urls'] = [
                'https://www.nomadfoods.com/wp-content/uploads/2018/08/placeholder-1-e1533569576673-960x960.png']

        if item['name'] != 'Loading...' and item['name'] != 'None':
            yield item

        print(response.body)

        raise scrapy.exceptions.CloseSpider("Unknown error")
