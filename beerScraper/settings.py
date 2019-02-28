BOT_NAME = 'beerScraper'

SPLASH_URL = 'http://192.168.99.100:8050'

DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

SPIDER_MODULES = ['beerScraper.spiders']
NEWSPIDER_MODULE = 'beerScraper.spiders'

DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'

SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

ITEM_PIPELINES = {
    'scrapy.pipelines.images.ImagesPipeline': 1,
    'beerScraper.pipelines.DuplicatesPipeline': 300,
    'beerScraper.pipelines.JsonWriterPipeline': 500
}

IMAGES_STORE = './images'


IMAGES_URLS_FIELD = 'image_urls'
IMAGES_RESULT_FIELD = 'images'

USER_AGENT = 'beerRecognizer (not yet on github)'

DOWNLOAD_TIMEOUT = 90