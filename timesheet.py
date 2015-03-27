#!/usr/bin/python
# -*- coding: utf-8 -*-
# @author Pablo Endres <epablo@pabloendres.com>
# Based on toggl_target (https://github.com/mos3abof/toggl_target) by @mos3abof

import os
import sys
import config
import requests
import dataset
import csv

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


def print_csv(entry_list, start='', stop='', client='No_client'):
    """

    :param entry_list, start='', stop='', client='No client',
    :return:
    """

    if client == '':
        client = 'No_client'

    filename = config.DATA_DIR + "/" + client + ".csv"
    with open(filename, 'w') as f:
        try:
            print "writing " + filename
            writer = csv.writer(f, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(("Client: ", client))
            writer.writerow(("Period: ", "%s - %s" % (start, stop)))
            writer.writerow((""))

            writer.writerow(("date", "start", "stop", "duration_dec"))
            for entry in entry_list:
                writer.writerow((entry['start'],  entry['start_time'],  entry['stop_time'],  entry['duration_dec']))
        finally:
            f.close()


def main():
    w = workingtime.WorkingTime(config.WORKING_HOURS_PER_DAY, config.BUSINESS_DAYS, config.WEEK_DAYS)
    r = api.ReportAPI(config.API_TOKEN, config.TIMEZONE, config.WORKSPACE_ID)

    start = w.month_start
    stop = w.month_end

    print "Hi"
    print "Checking Internet connectivity..."
    if not internet_on():
        print "OMG! There is no internet connection!"
        sys.exit()
    print "\nTrying to connect to Toggl, hang on!\n"
    try:
        time_entries = r.get_detailed_report(start, stop)
    except:
        print "OMG! Toggle request failed for some mysterious reason!"
        sys.exc_info()[0]
        sys.exit()

    # connecting to a SQLite database
    db_name = config.DATA_DIR + "/" + w.month_start.strftime("%Y-%m") + ".db"
    db_name_old = db_name + ".old"

    # Check if the db file already exists
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
        tt = toggltime.Toggletime(entry, roundup=config.ROUNDUP, align_time=config.ALIGN_TIME)
        tt.align_start_stop()
        tt.roundup()
        table.insert(tt.get_time_entry)

    # Get the list of clients
    clients = db.query('select distinct(client) from timesheet;')

    for c in clients:
        timeheet = db.query("select start, min(start_time) as start_time, max(stop_time) as stop_time, \
        sum(duration_dec) as duration_dec from timesheet where client='" + c['client'] + "' group by start;")
        print_csv(timeheet, start.date() ,stop.date(), c['client'])

    # select start, min(start_time) ,max(stop_time), sum(duration), sum(duration_dec) from timesheet where client='Vodafone' group by start ;


    # # Insert a new record.
    # table.insert(dict(name='John Doe', age=46, country='China'))
    #
    # # dataset will create "missing" columns any time you insert a dict with an unknown key
    # table.insert(dict(name='Jane Doe', age=37, country='France', gender='female'))
    # result = db.query('SELECT country, COUNT(*) c FROM user GROUP BY country')
    # for row in result:
    #     print(row['country'], row['c'])



if __name__ == '__main__':
    main()
