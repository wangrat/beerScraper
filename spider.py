import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'https://www.ratebeer.com/beer/rochefort-trappistes-10/2360',
    ]

    def parse(self, response):

        print(response.css('html').get())

        yield {
            'beerName': response.xpath('//h1[contains(@id, "beerName")]/text()')
        }

        next_page = response.css('a::attr("data-css-1wu499r")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)