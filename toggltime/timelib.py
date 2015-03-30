#!/usr/bin/python
# -*- coding: utf-8 -*-
# @author Pablo Endres <epablo@pabloendres.com>
# Based on toggl_target working time (https://github.com/mos3abof/toggl_target) by @mos3abof


from dateutil.relativedelta import relativedelta
from datetime import datetime


def now():
    return datetime.now() + relativedelta(microsecond=0)


def month_start(start=datetime.now()):
    return start + relativedelta(day=1, hour=0, minute=0, second=0, microsecond=0)


def month_end(end=datetime.now()):
    return end + relativedelta(day=31, hour=11, minute=59, second=59, microsecond=0)


def today():
    return datetime.now() + relativedelta(hour=0, minute=0, second=0, microsecond=0)


def last_month_start(start=datetime.now()):
    return start + relativedelta(months=-1, day=1, hour=0, minute=0, second=0, microsecond=0)

def last_month_end(end=datetime.now()):
    return end + relativedelta(months=-1, day=31, hour=11, minute=59, second=59, microsecond=0)


if __name__ == '__main__':
    import dateutil.parser


    print last_month_start().date()
    print last_month_end().date()
    start = dateutil.parser.parse('2015-03-15').date()
    print start

    import doctest

    doctest.testmod()

