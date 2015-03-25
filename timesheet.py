#!/usr/bin/python
# -*- coding: utf-8 -*-
# @author Pablo Endres <epablo@pabloendres.com>
# Based on toggl_target (https://github.com/mos3abof/toggl_target) by @mos3abof

import os
import sys
import config
import requests
import dataset

from togglapi import api
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
        print "r.get_detailed_report"
    except:
        print "OMG! Toggle request failed for some mysterious reason!"
        print "Good Bye Cruel World!"
        sys.exc_info()[0]
        sys.exit()

    print len(time_entries)

    # connecting to a SQLite database
    db_name = w.month_start.strftime("%Y-%m") + ".db"
    db_name_old = db_name + ".old"

    # Check if the db already exists

    ## delete only if file exists ##
    if os.path.exists(db_name):
        os.rename(db_name, db_name_old)
    elif os.path.exists(db_name) and os.path.exists(db_name_old):
        print("Deleting %s and renaming %s as %s." % (db_name_old, db_name, db_name_old))
        os.rename(db_name, db_name_old)
    else:
        print("Sorry, I can not remove %s file." % db_name)

    db = dataset.connect("sqlite:///"+db_name)

    # get a reference to the table
    table = db['timesheet']

    # Insert the entries in the DB
    for entry in time_entries:
        # Convert the tag list into csv string
        entry['tags'] = ', '.join(entry['tags'])
        table.insert(entry)

    # for entry in time_entries:
    #     print entry
    #     tt = toggltime.Toggletime(entry)
    #     tt.roundup()
    #     toggltime_list.append(tt)


    # # Insert a new record.
    # table.insert(dict(name='John Doe', age=46, country='China'))
    #
    # # dataset will create "missing" columns any time you insert a dict with an unknown key
    # table.insert(dict(name='Jane Doe', age=37, country='France', gender='female'))
    # result = db.query('SELECT country, COUNT(*) c FROM user GROUP BY country')
    # for row in result:
    #     print(row['country'], row['c'])




    #
    # print_csv(toggltime_list)
        # start = rounddown_start_time(entry['start'])
        # stop = roundup_finish_time(entry['stop'])
        # print "start: " +start + " -- " + entry['start']
        # print "start: " +stop + " -- " + entry['stop']

if __name__ == '__main__':
    main()
