#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright (C) 2016 John Zhao
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import re

import scrapy
from scrapy import signals

from proxy_spider.items import ProxySpiderItem


class XiciSpider(scrapy.spiders.Spider):
    """
    XiciSpider 是主要抓取代码，通过 start_urls 里面的连接，解析里面的 IP 地址
    """
    name = 'xici_spider'
    allowed_domains = ['xicidaili.com']
    start_urls = [
        'http://www.xicidaili.com/wt/1',
        'http://www.xicidaili.com/wt/2',
        'http://www.xicidaili.com/wt/3',
        'http://www.xicidaili.com/nn/1',
        'http://www.xicidaili.com/nn/2',
        'http://www.xicidaili.com/nn/3',
        'http://www.xicidaili.com/nt/1',
        'http://www.xicidaili.com/nt/2',
        'http://www.xicidaili.com/nt/3',
    ]

    # 减慢爬取速度
    download_delay = 30

    def __init__(self, success, failure):
        self.success = success
        self.failure = failure

    # crawler 会调用这个方法创建 spider 实例
    # 所以在里面注册一个关闭的回调
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        success = 0
        failure = 0

        spider = cls(success, failure)
        crawler.signals.connect(spider.closed_handler, signals.spider_closed)

        return spider

    def closed_handler(self, spider):
        spider.logger.warning('Spider closed, success: %d, failure: %d' % (self.success, self.failure))

    def get_or_none(self, array):
        if len(array) <= 0:
            return None
        else:
            return array[0]

    def parse(self, response):
        ip_list = response.xpath('//*[@id="ip_list"]/tr')

        for index, line in enumerate(ip_list):
            if index == 0:
                continue

            try:
                ip_item = ProxySpiderItem()
                ip_item['country'] = 'cn'
                ip_item['ip'] = self.get_or_none(line.xpath('td[2]/text()').extract())
                ip_item['port'] = self.get_or_none(line.xpath('td[3]/text()').extract())

                if self.get_or_none(line.xpath('td[4]/a/text()').extract()) is None:
                    ip_item['address'] = ''
                else:
                    ip_item['address'] = re.sub(r'[\n|\s]', '', self.get_or_none(line.xpath('td[4]/a/text()').extract()))

                ip_item['anonymous'] = self.get_or_none(line.xpath('td[5]/text()').extract())
                ip_item['proxy_type'] = self.get_or_none(line.xpath('td[6]/text()').extract())
                ip_item['auth_datetime'] = self.get_or_none(line.xpath('td[10]/text()').extract())

                self.success += 1
                yield ip_item
            except Exception as e:
                self.failure += 1
                self.logger.error(str(e))
