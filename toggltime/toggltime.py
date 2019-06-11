#!/usr/bin/python
# -*- coding: utf-8 -*-
# @author Pablo Endres <epablo+code@pabloendres.com>


from __future__ import division
from datetime import timedelta

import dateutil.parser


class Toggletime(object):
    """ Model Toggle time related items JSON time entries
        This should work with both items from the TogglAPI and the ReportAPI
    """

    def __init__(self, time_entry, roundup=0, align_time=0):
        """
        :param time_entry:
        :param roundup:

        :attrib: start datetime
        :return:
        """
        self.time_entry = time_entry
        self.ROUNDUP = roundup
        self.ALIGN_TIME = align_time

        # TimeAPI
        if 'project_hex_color' not in time_entry:
            self.duration = round(time_entry['duration'])
            self.duration_dec = self.sec_to_hours_dec(self.duration)
            self.start = dateutil.parser.parse(time_entry['start'])
            self.stop = dateutil.parser.parse(time_entry['stop'])
            self.type = 'TimeAPI'

            # Normalize the keys
            self.time_entry['tags'] = ''
            self.time_entry['start_time'] = self.start.time().isoformat()
            self.time_entry['stop_time'] = self.stop.time().isoformat()
            self.time_entry['duration_dec'] = self.duration_dec

        else:
            # ReportAPI
            self.duration = timedelta(microseconds=time_entry['dur']).total_seconds()
            self.duration = round(self.duration)
            self.duration_dec = self.sec_to_hours_dec(self.duration)
            self.start = dateutil.parser.parse(time_entry['start'])
            self.stop = dateutil.parser.parse(time_entry['end'])
            self.type = 'ReportAPI'

            # Normalize the keys
            del self.time_entry['dur']
            self.time_entry['duration'] = self.duration
            del self.time_entry['end']
            self.time_entry['stop'] = self.stop
            self.time_entry['tags'] = ', '.join(self.time_entry['tags'])
            self.time_entry['start_time'] = self.start.time().isoformat()
            self.time_entry['stop_time'] = self.stop.time().isoformat()
            self.time_entry['duration_dec'] = self.duration_dec

    def align_start(self):
        """
        Align the startup time
            self.ALIGN_TIME = 15  -> :00 :15 :30 :45
            self.ALIGN_TIME = 30  -> :00 :30
            self.ALIGN_TIME = 1  -> :00
            self.ALIGN_TIME = 0  -> do nothing
        """
        if self.ALIGN_TIME:
            self.start = self.start.replace(second=0)

        if self.ALIGN_TIME == 15:
            if 0 <= self.start.minute <= 10:
                self.start = self.start.replace(minute=0, second=0)
            elif 10 < self.start.minute <= 20:
                self.start = self.start.replace(minute=15, second=0)
            elif 20 < self.start.minute <= 40:
                self.start = self.start.replace(minute=30, second=0)
            elif 40 < self.start.minute <= 50:
                self.start = self.start.replace(minute=45, second=0)
            else:
                self.start = self.start.replace(hour=self.start.hour + 1, minute=0, second=0)
        elif self.ALIGN_TIME == 30:
            if 0 <= self.start.minute <= 15:
                self.start = self.start.replace(minute=0, second=0)
            elif 15 < self.start.minute <= 40:
                self.start = self.start.replace(minute=30, second=0)
            elif 40 < self.start.minute <= 59:
                self.start = self.start.replace(hour=self.start.hour + 1, minute=0, second=0)
        elif self.ALIGN_TIME == 1:
            if 0 <= self.start.minute < 6:
                self.start = self.start.replace(minute=0, second=0)
            elif 6 <= self.start.minute <= 59:
                self.start = self.start.replace(hour=self.start.hour + 1, minute=0, second=0)

    def align_stop(self):
        """
        Align the finish time
            self.ALIGN_TIME = 15  -> :00 :15 :30 :45
            self.ALIGN_TIME = 30  -> :00 :30
            self.ALIGN_TIME = 1  -> :00
            self.ALIGN_TIME = 0  -> do nothing
        """
        #to-do: add special case when 23:50

        if self.ALIGN_TIME:
            self.stop = self.stop.replace(second=0)

        if self.ALIGN_TIME == 15:
            if 0 < self.stop.minute <= 15:
                self.stop = self.stop.replace(minute=15, second=0)
            elif 15 < self.stop.minute <= 30:
                self.stop = self.stop.replace(minute=30, second=0)
            elif 30 < self.stop.minute <= 45:
                self.stop = self.stop.replace(minute=45, second=0)
            elif 45 < self.stop.minute <= 59:
                self.stop = self.stop.replace(hour=self.stop.hour + 1, minute=0, second=0)
        elif self.ALIGN_TIME == 30:
            if 0 < self.stop.minute <= 30:
                self.stop = self.stop.replace(minute=30, second=0)
            elif 30 < self.stop.minute <= 59:
                self.stop = self.stop.replace(hour=self.stop.hour + 1, minute=0, second=0)
        elif self.ALIGN_TIME == 1:
            if 0 <= self.stop.minute <= 5:
                self.stop = self.stop.replace(minute=0, second=0)
            elif 5 < self.stop.minute <= 59:
                self.stop = self.stop.replace(hour=self.stop.hour + 1, minute=0, second=0)

    def calculate_duration(self):
        """
        Calculate the duration: stop - start
        :return:
        """
        self.duration = self.stop - self.start
        self.duration = self.duration.total_seconds()
        self.duration_dec = self.sec_to_hours_dec(self.duration)

    def align_start_stop(self):
        """

        :return:
        """
        self.align_start()
        self.align_stop()
        self.calculate_duration()
        self.update_time_entry()

    def sec_to_hours_dec(self, time_sec):
        """
        :return: time in hours
        """
        return time_sec / 60 / 60

    def update_time_entry(self):
        """
        Update the dictionary
        :return:
        """
        self.time_entry['duration'] = round(self.duration)
        self.time_entry['duration_dec'] = round(self.duration_dec, 2)
        self.time_entry['start'] = self.start.isoformat()
        self.time_entry['stop'] = self.stop.isoformat()
        self.time_entry['start_time'] = self.start.time().isoformat()
        self.time_entry['stop_time'] = self.stop.time().isoformat()

    @property
    def get_time_entry(self):
        """

        :return: time_entry
        """
        self.time_entry['start'] = self.start.date().isoformat()
        self.time_entry['stop'] = self.stop.date().isoformat()
        return self.time_entry

    def roundup(self):
        # TODO: complete roundup

        # def myround(x, base=5):
        #     return int(base * round(float(x)/base))
        True


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    print "TogglAPI - test"
    tt = Toggletime({u'duronly': False, u'wid': 507341, u'description': u'Test entry', \
                     u'stop': u'2015-03-18T16:55:00+00:00', u'duration': 4500, u'pid': 5503294, \
                     u'start': u'2015-03-18T15:35:00+00:00', u'at': u'2015-03-18T16:48:04+00:00', \
                     u'billable': False, u'tid': 3399821, u'id': 210886825, u'uid': 676699})
    tt.ALIGN_TIME = 15
    print tt.start, tt.stop, tt.duration, tt.ROUNDUP, tt.ALIGN_TIME
    print tt.duration_dec, tt.stop - tt.start
    tt.align_start_stop()
    print tt.start, tt.stop, tt.duration, tt.duration_dec, tt.ALIGN_TIME
    print tt.duration_dec, tt.stop - tt.start
    tt.update_time_entry()
    print tt.get_time_entry

    print ""
    print "ReportAPI - test"
    tt = Toggletime({u'updated': u'2015-03-02T10:02:59+01:00', u'task': u'Other', u'end': u'2015-03-02T09:00:10+01:00', \
                     u'description': u'Other', u'project_color': u'13', u'tags': '', u'is_billable': True, \
                     u'pid': 5503294, u'cur': u'EUR', u'project': u'Proy1', u'start': u'2015-03-02T07:17:00+01:00', \
                     u'client': u'Client1', u'user': u'Max', u'billable': 0.0, u'tid': 3399820, \
                     u'project_hex_color': u'#bc2d07', u'dur': 7200000, u'use_stop': True, u'id': 205009936,
                     u'uid': 676699})
    tt.ALIGN_TIME = 15
    print tt.start, tt.stop, tt.duration, tt.ROUNDUP, tt.ALIGN_TIME
    print tt.duration_dec, tt.stop - tt.start
    tt.align_start_stop()
    print tt.start, tt.stop, tt.duration, tt.duration_dec, tt.ALIGN_TIME
    print tt.duration_dec, tt.stop - tt.start
    tt.update_time_entry()
    print tt.get_time_entry


