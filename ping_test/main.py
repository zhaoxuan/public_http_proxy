#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright (C) 2016 JohnZ
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

import socket
import datetime
import time
import sys
sys.path.insert(0, '..')

import ping
from proxy_spider.proxy_spider.models import PublicHttpProxyIp
"""
通过 ping 来验证 ip 是否可用
"""

def ping_ip(ip, timeout=2, count=4):
    is_alive = False

    for i in xrange(count):
        try:
            delay = ping.do_one(ip, timeout)
        except socket.gaierror, e:
            print "failed. (socket error: '%s')" % e[1]
            break

        if delay is None:
            is_alive = False
            delay = 0
        else:
            is_alive = True
            delay = delay * 1000

    return is_alive, delay


def test_http_proxy_ip(number=10):
    for r in PublicHttpProxyIp.select().order_by(PublicHttpProxyIp.update_datetime).limit(number):
        now = datetime.datetime.now()

        is_alive, delay = ping_ip(r.ip)
        r.is_alive = is_alive

        if is_alive:
            r.timeout = delay
        else:
            r.timeout = 0
        r.update_datetime = int(now.strftime('%y%m%d%H%M'))
        r.save()

        print 'Ping host: %s in %0.4fms ' % (r.ip, r.timeout)


while True:
    test_http_proxy_ip()
    time.sleep(1)
