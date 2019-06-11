#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author Pablo Endres <epablo@pabloendres.com>
# Based on toggl_target (https://github.com/mos3abof/toggl_target) by @mos3abof

import os
import sys
import config
import requests
import dataset
import csv
import getopt

from togglapi import api
from toggltime import toggltime
from toggltime import timelib
import dateutil.parser


version = "0.9"
url = "http://www.pabloendres.com/tools#timesheet"
verbose = False


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

    filename = config.DATA_DIR + "/" + timelib.year_month_only(start) + '-' + client + ".csv"
    with open(filename, 'w') as f:
        try:
            print "writing " + filename
            writer = csv.writer(f, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(("Client: ", client))
            writer.writerow(("Period: ", "%s - %s" % (start, stop)))
            writer.writerow((""))

            writer.writerow(("date", "start", "stop", "duration_dec"))
            for entry in entry_list:
                writer.writerow((entry['start'], entry['start_time'], entry['stop_time'], entry['duration_dec']))
        finally:
            f.close()


def usage(error_msg=''):
    """ Show usage options """

    global version
    global url

    print error_msg
    print ""
    print "timeheet v" + version + "\t" + url
    print "usage:  timeheet.py [OPTION...] \n"
    print "     -h, --help                          display this help"
    print "     -t [token], --api-token=token       Toggl API token"
    print "     -d dirname, --data-dir=dirname      directory where to store results and local database"
    print "     -r value,   --roundup=value         round up precision"
    print "     -a,         --align-time=value      Align the start - end time of each entry"
    print "     -z,         --time-zone=tz          Timezone to use. Format \"+HH:MM\""
    print "     -w,         --workspace-id=id       Toogl Worskpace ID"
    print "     -s,         --start=YYYY-MM-DD      Start of the report - default: last month"
    print "     -e,         --end=YYYY-MM-DD        End of the report - default: end of last month"
    print ""
    print ""
    print "ROUNDUP = 15  -> :00 :15 :30 :45; ROUNDUP = 30  -> :00 :30; ROUNDUP= 1  -> :00, 0 -> don't round up"
    print "ALIGN = 15  -> :00 :15 :30 :45; ALIGN = 30  -> :00 :30; ALIGN= 1  -> :00, 0 -> don't round up"
    print ""
    exit()


def main():
    # 'API_TOKEN': '38bf888afc4203fb443a5503b1f36252',
    # 'DATA_DIR': 'data',
    # 'ROUNDUP': 15,
    # ALIGN_TIME': 15
    # 'TIMEZONE': '+02:00',
    # 'WORKSPACE_ID': '507341',

    start = False
    stop = False

    try:
        opts, args = getopt.gnu_getopt(
            sys.argv[1:], "hd:r:a:t:z:w:s:e:",
            ["help", "api-token=", "data-dir=", "roundup=", "align-time=", "time-zone=", \
             "workspace-id=", "start=", "end="])
    except getopt.GetoptError, e:
        usage(e.msg)

    for o, arg in opts:
        if o == "-h" or o == "--help":
            usage()
            sys.exit(0)
        elif o == "-t" or o == "--api-token":
            config.API_TOKEN = arg
        elif o == "-d" or o == "--data-dir":
            config.DATA_DIR = arg
        elif o == "-r" or o == "--roundup":
            config.ROUNDUP = arg
        elif o == "-a" or o == "--align-time":
            config.ALIGN_TIME = arg
        elif o == "-z" or o == "--time-zone":
            config.TIMEZONE = arg
        elif o == "-w" or o == "--workspace-id":
            config.WORKSPACE_ID = arg
        elif o == "-s" or o == "--start":
            start = arg
        elif o == "-e" or o == "--end":
            stop = arg

    if not start and not stop:
        start = timelib.last_month_start()
        stop = timelib.last_month_end()
    elif start and not stop:
        start = dateutil.parser.parse(start)
        stop = timelib.month_end(start)
    elif not start and stop:
        stop = dateutil.parser.parse(stop)
        start = timelib.month_start(stop)
    else:
        start = dateutil.parser.parse(start)
        stop = dateutil.parser.parse(stop)

    r = api.ReportAPI(config.API_TOKEN, config.TIMEZONE, config.WORKSPACE_ID)

    print "Hi"
    print "Checking Internet connectivity..."
    if not internet_on():
        print "OMG! There is no internet connection!"
        sys.exit()
    print "\nTrying to connect to Toggl, hang on!\n"
    try:
        print ("Getting reports for entries between %s and %s\n" % (start, stop))
        time_entries = r.get_detailed_report(start, stop)
    except Exception as e:
        print "OMG! Toggle request failed for some mysterious reason!"
        print e.message
        sys.exc_info()[0]
        sys.exit()

    # connecting to a SQLite database
    db_name = config.DATA_DIR + "/" + start.strftime("%Y-%m") + ".db"
    db_name_old = db_name + ".old"

    # Check if the db file already exists
    if os.path.exists(db_name):
        os.rename(db_name, db_name_old)
    elif os.path.exists(db_name) and os.path.exists(db_name_old):
        print("Deleting %s and renaming %s as %s." % (db_name_old, db_name, db_name_old))
        os.rename(db_name, db_name_old)
    else:
        print("Sorry, I can not remove %s file." % db_name)

    db = dataset.connect("sqlite:///" + db_name)

    # Create the table without a primary_key and grab a reference
    table = db.create_table('timesheet', primary_id=False)


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
        print_csv(timeheet, start.date(), stop.date(), c['client'])

def print_config():
    from pprint import pprint

    pprint(vars(config))

if __name__ == '__main__':
    main()
