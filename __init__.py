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

from cocaine.worker import Worker
from cocaine.services import Service
from cocaine.decorators import http

logger = Service("logging::v2")
old_logger = Service("logging")

counter = 0
old_counter = 0
verbosity = 4
attributes = [
    ["attribute1", "attribute1_value"],
    ["attrinute2", "attribute2_value"],
    ["attrinute3", "attribute3_value"],
    ["attrinute4", "attribute4_value"],
    ["attrinute5", "attribute5_value"],
    ["attrinute6", 42],
    ["attrinute7", True]
]


def get_logger():
    global counter
    counter = counter + 1
    if counter % 50 == 0:
        logger.disconnect()
    return logger


def get_old_logger():
    global old_counter
    old_counter = old_counter + 1
    if old_counter % 50 == 0:
        old_logger.disconnect()
    return old_logger


@http
def new_emit_ack(request, response):
    channel = yield get_logger().get("logger_test_app")
    for i in xrange(1000):
        yield channel.tx.emit_ack(verbosity, "log string", attributes)
    for i in xrange(1000):
        yield channel.rx.get()
    response.write_head(200, {})
    response.write("logging test app python")


@http
def new_emit(request, response):
    channel = yield get_logger().get("logger_test_app")
    for i in xrange(1000):
        yield channel.tx.emit(verbosity, "log string", attributes)
    response.write_head(200, {})
    response.write("logging test app python")


@http
def new_emit_ack_plain(request, response):
    l = get_logger()
    for i in xrange(1000):
        channel = yield l.emit_ack(verbosity, "logger_test_app", "log string", attributes)
        yield channel.rx.get()
    response.write_head(200, {})
    response.write("logging test app python")


@http
def new_emit_plain(request, response):
    l = get_logger()
    for i in xrange(1000):
        channel = yield l.emit(verbosity, "logger_test_app", "log string", attributes)
        yield channel.rx.get()
    response.write_head(200, {})
    response.write("logging test app python")


@http
def old_emit(request, response):
    l = get_old_logger()
    for i in xrange(1000):
        channel = yield l.emit(verbosity, "logger_test_app", "log string", attributes)
        yield channel.rx.get()
    response.write_head(200, {})
    response.write("logging test app python")


def main():
    w = Worker()
    w.on("new_emit_ack", new_emit_ack)
    w.on("new_emit", new_emit)
    w.on("new_emit_ack_plain", new_emit_ack_plain)
    w.on("new_emit_plain", new_emit_plain)
    w.on("old_emit", old_emit)
    w.run()


if __name__ == '__main__':
    main()
