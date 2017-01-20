# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProxySpiderItem(scrapy.Item):
    # define the fields for your item here like:
    country = scrapy.Field()
    ip = scrapy.Field()
    port = scrapy.Field()
    address = scrapy.Field()
    anonymous = scrapy.Field()
    proxy_type = scrapy.Field()
    auth_datetime = scrapy.Field()
    pass
