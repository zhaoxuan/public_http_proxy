# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import datetime

from proxy_spider.models import PublicHttpProxyIp


class ProxySpiderPipeline(object):
    def process_item(self, item, spider):
        ip = item['ip']
        port = int(item['port'])

        if item['anonymous'] == u'高匿':
            anonymous = True
        else:
            anonymous = False

        at = datetime.datetime.strptime(item['auth_datetime'], '%y-%m-%d %H:%M')
        auth_datetime = int(at.strftime('%y%m%d%H%M'))
        now = datetime.datetime.now()

        if PublicHttpProxyIp.select().where(PublicHttpProxyIp.ip == ip, PublicHttpProxyIp.port == port).count() == 0:
            PublicHttpProxyIp.create(
                ip=ip,
                port=port,
                country=item['country'],
                address=item['address'],
                anonymous=anonymous,
                proxy_type=item['proxy_type'],
                auth_datetime=auth_datetime,
                is_alive=True,
                timeout=0,
                create_datetime=int(now.strftime('%y%m%d%H%M')),
                update_datetime=int(now.strftime('%y%m%d%H%M'))
            )

        else:
            query = PublicHttpProxyIp.update(
                country=item['country'],
                address=item['address'],
                anonymous=anonymous,
                proxy_type=item['proxy_type'],
                auth_datetime=auth_datetime,
                update_datetime=int(now.strftime('%y%m%d%H%M'))
            ).where(PublicHttpProxyIp.ip == ip, PublicHttpProxyIp.port == port)
            query.execute()

        return item
