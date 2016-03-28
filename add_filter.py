#!/usr/bin/env python

#    Copyright (c) 2014 Anton Tyurin <noxiouz@yandex.ru>
#    This file is part of Cocaine.
#
#    Cocaine is free software; you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    Cocaine is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#

from cocaine.services import Service
from tornado.ioloop import IOLoop
from tornado import gen

logger = Service("logging::v2")


@gen.coroutine
def main():
    yield logger.connect()
    logger.set_cluster_filter("logger_test_app", ["&&", ["==", "attribute1", "attribute1_value"], ["==", "attribute2", "attribute2_value"]], 3600)
    channel = yield logger.list_filters()
    data = yield channel.rx.get()
    print data

if __name__ == '__main__':
    IOLoop.current().run_sync(main)
