# Scrapy settings for amazonbook project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

import sys
import os
from os.path import dirname

BOT_NAME = 'beerScraper'

SPLASH_URL = 'http://0.0.0.0:8050'

DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}


SPIDER_MODULES = ['beerScraper.spiders']
NEWSPIDER_MODULE = 'beerScraper.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'amazonbook (+http://www.yourdomain.com)'


ITEM_PIPELINES = {
    #'beerScraper.pipelines.JsonWithEncodingPipeline': 300,
    #'amazonbook.pipelines.RedisPipeline': 301,
}

DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'

SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}


LOG_LEVEL = 'INFO'

DOWNLOAD_DELAY = 1
