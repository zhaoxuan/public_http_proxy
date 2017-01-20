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

from peewee import *

DATABASE = MySQLDatabase('public_http_proxy', **{'host': 'beijing.iok.la', 'password': '123456', 'port': 23306, 'user': 'john'})
DATABASE.connect()


class PublicHttpProxyIp(Model):
    ip = CharField(max_length=128)
    port = IntegerField()
    country = CharField(max_length=128, null=True)
    address = CharField(max_length=128, null=True)
    anonymous = BooleanField(default=True)
    proxy_type = CharField(max_length=128, null=True)
    auth_datetime = BigIntegerField(null=True)
    is_alive = BooleanField(default=True)
    timeout = IntegerField(null=True)
    create_datetime = BigIntegerField(null=True)
    update_datetime = BigIntegerField(null=True)

    class Meta:
        database = DATABASE


if __name__ == '__main__':
    PublicHttpProxyIp.create_table()
