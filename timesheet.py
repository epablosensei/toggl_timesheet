#!/usr/bin/python
# -*- coding: utf-8 -*-
# @author Pablo Endres <epablo@pabloendres.com>
# Based on toggl_target (https://github.com/mos3abof/toggl_target) by @mos3abof

import os
import sys
import config
import requests

from togglapi import api
from toggltarget import target
from workingtime import workingtime
from toggltime import toggltime
from datetime import datetime


def internet_on():
    """Checks if internet connection is on by connecting to Google"""
    try:
        requests.get('http://www.google.com', timeout=10)
        return True
    except requests.exceptions.ConnectionError:
        return False
    except:
        return False


def print_csv(toggltime_list):
    """

    :param toggltime_list:
    :return:
    """
    # print the headers
    print "date,start,stop,duration,duration_dec"
    for tt in toggltime_list:
        print("%s,%s,%s,%s,%s", tt.start.strftime("%Y-%m-%d"), tt.start.strftime("%H:%M"), tt.stop.strftime("%H:%M"),
        tt.duration, tt.duration_dec)

def main():
    w = workingtime.WorkingTime(config.WORKING_HOURS_PER_DAY, config.BUSINESS_DAYS, config.WEEK_DAYS)
    # a = api.TogglAPI(config.API_TOKEN, config.TIMEZONE)
    r = api.ReportAPI(config.API_TOKEN, config.TIMEZONE, config.WORKSPACE_ID)

    time_entries = []
    toggltime_list = []

    print "Hi"
    print "Checking Internet connectivity..."
    if not internet_on():
        print "OMG! There is no internet connection!"
        print "Good Bye Cruel World!"
        sys.exit()
    print "Internet seems fine!"
    print "\nTrying to connect to Toggl, hang on!\n"
    try:
        # time_entries = a.get_tracked_entries(start_date=w.month_start, end_date=w.month_end)
        time_entries = r.get_detailed_report(since=w.month_start, until=w.month_end)
    except:
        print "OMG! Toggle request failed for some mysterious reason!"
        print "Good Bye Cruel World!"
        sys.exit()

    print len(time_entries)
    # for entry in time_entries:
    #     print entry
    #     tt = toggltime.Toggletime(entry)
    #     tt.roundup()
    #     toggltime_list.append(tt)
    #
    # print_csv(toggltime_list)
        # start = rounddown_start_time(entry['start'])
        # stop = roundup_finish_time(entry['stop'])
        # print "start: " +start + " -- " + entry['start']
        # print "start: " +stop + " -- " + entry['stop']






    sys.exit()

    t.required_hours = w.required_hours_this_month
    t.tolerance = config.TOLERANCE_PERCENTAGE

    print "So far you have tracked",
    print "Total days left till deadline : {}".format(w.days_left_count)
    print "\nThis month targets [Required (minimum)] : {} ({})".format(w.required_hours_this_month,
                                                                       w.required_hours_this_month - (
                                                                       w.required_hours_this_month * config.TOLERANCE_PERCENTAGE))
    print "\nTo achieve the minimum:\n\tyou should log {0:.2f} hours every business day".format(normal_min_hours)
    print "\tor log {0:.2f} hours every day".format(crunch_min_hours)
    print "\tleft is : {0:.2f}".format(
        (w.required_hours_this_month - (w.required_hours_this_month * config.TOLERANCE_PERCENTAGE)) - t.achieved_hours)

    normal_required_hours, crunch_required_hours = t.get_required_daily_hours(w.business_days_left_count,
                                                                              w.days_left_count)

    print "\nTo achieve the required :\n\tyou should log {0:.2f} hours every business day".format(normal_required_hours)
    print "\tor log {0:.2f} hours every day".format(crunch_required_hours)
    print "\tleft is : {0:.2f}".format(w.required_hours_this_month - t.achieved_hours)
    print "\nHow your progress looks:"
    bar = percentile_bar(t.achieved_percentage, config.TOLERANCE_PERCENTAGE)
    print bar


if __name__ == '__main__':
    main()
