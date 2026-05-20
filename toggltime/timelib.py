#!/usr/bin/python
# -*- coding: utf-8 -*-
# @author Pablo Endres <epablo@pabloendres.com>
# Based on toggl_target working time (https://github.com/mos3abof/toggl_target) by @mos3abof


from datetime import date, datetime

from dateutil.relativedelta import relativedelta


def now() -> datetime:
    return datetime.now() + relativedelta(microsecond=0)


def month_start(dt: datetime = datetime.now()) -> datetime:
    return dt + relativedelta(day=1, hour=0, minute=0, second=0, microsecond=0)


def month_end(end: datetime = datetime.now()) -> datetime:
    return end + relativedelta(day=31, hour=11, minute=59, second=59, microsecond=0)


def today() -> datetime:
    return datetime.now() + relativedelta(hour=0, minute=0, second=0, microsecond=0)


def last_month_start(dt: datetime = datetime.now()) -> datetime:
    return dt + relativedelta(months=-1, day=1, hour=0, minute=0, second=0, microsecond=0)


def last_month_end(end: datetime = datetime.now()) -> datetime:
    return end + relativedelta(months=-1, day=31, hour=11, minute=59, second=59, microsecond=0)


def year_month_only(dt: datetime | date = datetime.now()) -> str:
    tmp = dt + relativedelta(day=1, hour=0, minute=0, second=0, microsecond=0)
    return tmp.strftime("%Y-%m")

if __name__ == '__main__':
    import dateutil.parser

    print(last_month_start().date())
    print(last_month_end().date())
    start = dateutil.parser.parse('2015-03-15').date()
    print(start)
    print(year_month_only())

    import doctest

    doctest.testmod()
