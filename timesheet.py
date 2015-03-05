#!/usr/bin/python
# -*- coding: utf-8 -*-
#@author Pablo Endres <epablo@pabloendres.com>
# Based on toggl_target (https://github.com/mos3abof/toggl_target) by @mos3abof

import os
import sys
import config
import requests

from togglapi import api
from toggltarget import target
from workingtime import workingtime


def internet_on():
    """Checks if internet connection is on by connecting to Google"""
    try:
        requests.get('http://www.google.com', timeout=10)
        return True
    except requests.exceptions.ConnectionError:
        return False
    except:
        return False

def main_timesheet():
    w = workingtime.WorkingTime(config.WORKING_HOURS_PER_DAY, config.BUSINESS_DAYS, config.WEEK_DAYS)
    a = api.TogglAPI(config.API_TOKEN, config.TIMEZONE)
    

def main():
    w = workingtime.WorkingTime(config.WORKING_HOURS_PER_DAY, config.BUSINESS_DAYS, config.WEEK_DAYS)
    a = api.TogglAPI(config.API_TOKEN, config.TIMEZONE)
    t = target.Target()

    print "Hi"
    print "Checking Internet connectivity..."
    if not internet_on():
        print "OMG! There is no internet connection!"
        print "Good Bye Cruel World!"
        sys.exit()
    print "Internet seems fine!"
    print "\nTrying to connect to Toggl, hang on!\n"
    try:
        t.achieved_hours = a.get_hours_tracked(start_date=w.month_start, end_date=w.month_end)
    except:
        print "OMG! Toggle request failed for some mysterious reason!"
        print "Good Bye Cruel World!"
        sys.exit()

    t.required_hours = w.required_hours_this_month
    t.tolerance      = config.TOLERANCE_PERCENTAGE

    print "So far you have tracked",
    print "Total days left till deadline : {}".format(w.days_left_count)
    print "\nThis month targets [Required (minimum)] : {} ({})".format(w.required_hours_this_month, w.required_hours_this_month - (w.required_hours_this_month * config.TOLERANCE_PERCENTAGE))
    print "\nTo achieve the minimum:\n\tyou should log {0:.2f} hours every business day".format(normal_min_hours)
    print "\tor log {0:.2f} hours every day".format(crunch_min_hours)
    print "\tleft is : {0:.2f}".format((w.required_hours_this_month - (w.required_hours_this_month * config.TOLERANCE_PERCENTAGE)) - t.achieved_hours)

    normal_required_hours, crunch_required_hours = t.get_required_daily_hours(w.business_days_left_count, w.days_left_count)

    print "\nTo achieve the required :\n\tyou should log {0:.2f} hours every business day".format(normal_required_hours)
    print "\tor log {0:.2f} hours every day".format(crunch_required_hours)
    print "\tleft is : {0:.2f}".format(w.required_hours_this_month - t.achieved_hours)
    print "\nHow your progress looks:"
    bar = percentile_bar(t.achieved_percentage, config.TOLERANCE_PERCENTAGE)
    print bar

if __name__ == '__main__':
    main()
