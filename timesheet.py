#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author Pablo Endres <epablo@pabloendres.com>
# Based on toggl_target (https://github.com/mos3abof/toggl_target) by @mos3abof

import csv
import getopt
import os
import sys
from pprint import pprint
from typing import NoReturn

import dataset
import dateutil.parser
import requests

import config
from togglapi import api
from toggltime import timelib
from toggltime import toggltime


VERSION = "0.9.2"
URL = "http://www.pabloendres.com/tools#timesheet"
VERBOSE = False


def internet_on() -> bool:
    """Checks if internet connection is on by connecting to Google"""
    try:
        requests.get('http://www.google.com', timeout=10)
        return True
    except requests.exceptions.ConnectionError:
        return False
    except OSError:
        return False


def print_csv(entry_list, start, stop, client: str = 'No_client') -> None:
    """

    :param entry_list, start='', stop='', client='No client',
    :return:
    """

    if client == '':
        client = 'No_client'

    filename = config.DATA_DIR + "/" + timelib.year_month_only(start) + '-' + client + ".csv"
    with open(filename, 'w', encoding='utf-8') as f:
        print("writing " + filename)
        writer = csv.writer(f, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(("Client: ", client))
        writer.writerow(("Period: ", f"{start} - {stop}"))
        writer.writerow((""))
        writer.writerow((
            "consultant", "start date", "start time",
            "stop date", "stop time", "time (h)", "duration_dec"
        ))
        for entry in entry_list:
            writer.writerow((
                entry['user'], entry['start'], entry['start_time'],
                '', entry['stop_time'], '', entry['duration_dec']
            ))


def usage(error_msg: str = '') -> NoReturn:
    """ Show usage options """

    print(error_msg)
    print("")
    print("timesheet v" + VERSION + "\t" + URL)
    print("usage:  timesheet.py [OPTION...] \n")
    print("     -h, --help                          display this help")
    print("     -t [token], --api-token=token       Toggl API token")
    print("     -d dirname, --data-dir=dirname      "
          "directory where to store results and local database")
    print("     -r value,   --roundup=value         round up precision")
    print("     -a,         --align-time=value      Align the start - end time of each entry")
    print("     -z,         --time-zone=tz          Timezone to use. Format \"+HH:MM\"")
    print("     -w,         --workspace-id=id       Toggl Workspace ID")
    print("     -s,         --start=YYYY-MM-DD      Start of the report - default: last month")
    print("     -e,         --end=YYYY-MM-DD        End of the report - default: end of last month")
    print("     -p,         --per-project           "
          "create separate CSVs per project under each client")
    print("     -f,         --full                  export all entries to a single full.csv file")
    print("     -m,         --monthly               export daily totals per user to monthly CSV")

    print("")
    print("-f exports every individual time entry (raw data) to a single CSV")
    print("-m exports one row per day per user (daily totals across all clients/projects)")
    print("")
    print("ALIGN_TIME = 15 -> snaps start/stop to :00 :15 :30 :45; "
          "ALIGN_TIME = 30 -> :00 :30; ALIGN_TIME = 1 -> :00; 0 -> off")
    print("ROUNDUP = 15 -> rounds duration up to next 15-min interval (extends stop); "
          "0 -> off. Redundant when same value as ALIGN_TIME.")
    print("")
    sys.exit()


def main():
    # 'API_TOKEN': '38bf888afc4203fb443a5503b1f36252',
    # 'DATA_DIR': 'data',
    # 'ROUNDUP': 15,
    # 'ALIGN_TIME': 15
    # 'TIMEZONE': '+02:00',
    # 'WORKSPACE_ID': '507341',

    start_str: str | None = None
    stop_str: str | None = None
    per_project = False
    full = False
    monthly = False

    try:
        opts, _ = getopt.gnu_getopt(
            sys.argv[1:], "hd:r:a:t:z:w:s:e:pfm",
            ["help", "api-token=", "data-dir=", "roundup=", "align-time=", "time-zone=",
             "workspace-id=", "start=", "end=", "per-project", "full", "monthly"])
    except getopt.GetoptError as e:
        usage(e.msg)

    for o, arg in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-t", "--api-token"):
            config.API_TOKEN = arg
        elif o in ("-d", "--data-dir"):
            config.DATA_DIR = arg
        elif o in ("-r", "--roundup"):
            config.ROUNDUP = int(arg)
        elif o in ("-a", "--align-time"):
            config.ALIGN_TIME = int(arg)
        elif o in ("-z", "--time-zone"):
            config.TIMEZONE = arg
        elif o in ("-w", "--workspace-id"):
            config.WORKSPACE_ID = arg
        elif o in ("-s", "--start"):
            start_str = arg
        elif o in ("-e", "--end"):
            stop_str = arg
        elif o in ("-p", "--per-project"):
            per_project = True
        elif o in ("-f", "--full"):
            full = True
        elif o in ("-m", "--monthly"):
            monthly = True

    if not start_str and not stop_str:
        start = timelib.last_month_start()
        stop = timelib.last_month_end()
    elif start_str and not stop_str:
        start = dateutil.parser.parse(start_str)
        stop = timelib.month_end(start)
    elif not start_str and stop_str:
        stop = dateutil.parser.parse(stop_str)
        start = timelib.month_start(stop)
    else:
        assert start_str is not None and stop_str is not None
        start = dateutil.parser.parse(start_str)
        stop = dateutil.parser.parse(stop_str)

    r = api.ReportAPI(config.API_TOKEN, config.TIMEZONE, config.WORKSPACE_ID)

    print("Hi")
    print("Checking Internet connectivity...")
    if not internet_on():
        print("OMG! There is no internet connection!")
        sys.exit()
    print("\nTrying to connect to Toggl, hang on!\n")
    try:
        print(f"Getting reports for entries between {start} and {stop}\n")
        time_entries = r.get_detailed_report(start, stop)
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response is not None else None
        if status == 401:
            print("Authentication failed — check your API token in config.py")
        elif status == 429:
            print("Toggl API rate limit reached — try again in a few seconds")
        else:
            print(f"Toggl API error: {e}")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print("Toggl API request timed out — check your connection and try again")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Toggl API request failed: {e}")
        sys.exit(1)

    # connecting to a SQLite database
    db_name = config.DATA_DIR + "/" + start.strftime("%Y-%m") + ".db"
    db_name_old = db_name + ".old"

    # Rotate the db: move any existing db to .old before creating a fresh one
    if os.path.exists(db_name):
        if os.path.exists(db_name_old):
            os.remove(db_name_old)
        os.rename(db_name, db_name_old)

    db = dataset.connect("sqlite:///" + db_name)

    # Create the table without a primary_key and grab a reference
    table = db.create_table('timesheet', primary_id=False)


    # Insert the entries in the DB
    for entry in time_entries:
        tt = toggltime.Toggletime(entry, roundup=config.ROUNDUP, align_time=config.ALIGN_TIME)
        tt.align_start_stop()
        tt.roundup()
        table.insert(tt.get_time_entry)

    users = db.query('SELECT DISTINCT(user) FROM timesheet;')

    # Get the list of clients
    if not full and not per_project and not monthly:
        clients = list(db.query('select distinct(client) from timesheet;'))

        for c in clients:
            client_name = str(c['client'] or '')
            timesheet = db.query(
                "SELECT user, start, MIN(start_time) AS start_time, MAX(stop_time) AS stop_time, "
                "SUM(duration_dec) AS duration_dec "
                "FROM timesheet WHERE client = :client GROUP BY start;",
                client=client_name
            )
            print_csv(timesheet, start.date(), stop.date(), client_name)

    if per_project:
        clients = list(db.query('SELECT DISTINCT(client) FROM timesheet;'))

        # Create a CSV file per per project for each user
        for u in users:
            user_name = str(u['user'] or '')
            # user_name in camel case
            user_name_cc = user_name.replace(" ", "_").lower()
            print(f"Creating CSVs for {user_name}")

            for c in clients:
                client_name = str(c['client'] or '')
                print(f"Working on {client_name}/{user_name}")

                projects = db.query(
                    "SELECT DISTINCT(project) FROM timesheet "
                    "WHERE client = :client and user = :user;",
                    client=client_name, user=user_name
                )

                for p in projects:
                    project_name = str(p['project'] or '')

                    entries = db.query(
                        "SELECT user, start, "
                        "MIN(start_time) AS start_time, MAX(stop_time) AS stop_time, "
                        "SUM(duration_dec) AS duration_dec "
                        "FROM timesheet "
                        "WHERE client = :client AND project = :project AND user = :user "
                        "GROUP by start;",
                        client=client_name, project=project_name, user=user_name
                    )

                    ym = timelib.year_month_only(start)
                    filename = f"{ym}-{client_name}-{project_name}-{user_name_cc}.csv"

                    filepath = os.path.join(config.DATA_DIR, filename)
                    with open(filepath, 'w', encoding='utf-8') as f:
                        print("Writing " + filepath)
                        writer = csv.writer(f, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
                        writer.writerow(("Client:", client_name))
                        writer.writerow(("Project:", project_name))
                        writer.writerow(("Period:", f"{start} - {stop}"))
                        writer.writerow(("User:", user_name))
                        writer.writerow((""))
                        writer.writerow(())
                        writer.writerow((
                            "consultant", "start date", "start time",
                            "stop date", "stop time", "time (h)", "duration_dec"
                        ))
                        for entry in entries:
                            writer.writerow((
                                entry['user'], entry['start'], entry['start_time'],
                                '', entry['stop_time'], '', entry['duration_dec']
                            ))
    if full:
        full_entries = db.query(
            "SELECT user, start, MIN(start_time) AS start_time, MAX(stop_time) AS stop_time, "
            "SUM(duration_dec) AS duration_dec "
            "FROM timesheet GROUP BY user, start;"
        )
        filename = os.path.join(config.DATA_DIR, timelib.year_month_only(start) + "-full.csv")
        with open(filename, 'w', encoding='utf-8') as f:
            print("Writing " + filename)
            writer = csv.writer(f, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow((
                "consultant", "start date", "start time",
                "stop date", "stop time", "time (h)", "duration_dec"
            ))
            for entry in full_entries:
                writer.writerow((
                    entry['user'], entry['start'], entry['start_time'],
                    '', entry['stop_time'], '', entry['duration_dec']
                ))



    if monthly:
        user_list = list(db.query('SELECT DISTINCT(user) FROM timesheet;'))
        for u in user_list:
            user_name = str(u['user'] or 'Unknown')
            user_name_cc = user_name.replace(" ", "_").lower()

            monthly_entries = db.query(
                "SELECT user, start, MIN(start_time) AS start_time, "
                "MAX(stop_time) AS stop_time, SUM(duration_dec) AS duration_dec "
                "FROM timesheet WHERE user = :user "
                "GROUP BY start ORDER BY start;",
                user=user_name
            )

            ym = timelib.year_month_only(start)
            filepath = os.path.join(config.DATA_DIR, f"{ym}-{user_name_cc}-monthly.csv")
            with open(filepath, 'w', encoding='utf-8') as f:
                print(f"Writing {filepath}")
                writer = csv.writer(f, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
                writer.writerow(("User:", user_name))
                writer.writerow(("Period:", f"{start.date()} - {stop.date()}"))
                writer.writerow((""))
                writer.writerow((
                    "consultant", "start date", "start time",
                    "stop time", "duration_dec"
                ))
                for entry in monthly_entries:
                    writer.writerow((
                        entry['user'], entry['start'], entry['start_time'],
                        entry['stop_time'], entry['duration_dec']
                    ))


def print_config():
    pprint(vars(config))

if __name__ == '__main__':
    main()
