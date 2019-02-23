import scrapy
import scrapy_splash


# this example needs the scrapyjs package: pip install scrapyjs
# it also needs a splash instance running in your env or on Scrapy Cloud (https://github.com/scrapinghub/splash)
class SplashSpider(scrapy.Spider):
    name = 'splash-spider'
    download_delay = 3

    def start_requests(self):
        yield scrapy_splash.SplashRequest('https://www.ratebeer.com/beer/rochefort-trappistes-10/2360', self.parse,
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
        for quote in response.css('[data-css-1wu499r]'):
            yield {
                'text': quote.css('[data-css-j2elum]').extract_first()
            }
