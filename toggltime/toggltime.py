#!/usr/bin/python
# -*- coding: utf-8 -*-
#@author Pablo Endres <epablo+code@pabloendres.com>


from datetime import datetime
import dateutil.parser
from dateutil.relativedelta import relativedelta

class Toggletime(object):
    """ Model Toggle JSON time entries """


    def __init__(self, time_entry, roundup = 0):
        """
        :param time_entry:
        :param roundup:

        :attrib: start datetime
        :return:
        """
        self.time_entry = time_entry
        self.ROUNDUP = roundup

        # print time_entry

        # {u'duronly': False, u'wid': 507341, u'description': u'Test entry', u'stop': u'2015-03-18T16:45:00+00:00',
        # u'duration': 4500, u'pid': 5503294, u'start': u'2015-03-18T15:30:00+00:00', u'at': u'2015-03-18T16:48:04+00:00',
        # u'billable': False, u'tid': 3399821, u'id': 210886825, u'uid': 676618}


        self.description = time_entry['description']
        # self.duration = time_entry['duration']
        self.duration = relativedelta(seconds=time_entry['duration'])
        self.duration_dec = self.sec_to_hours_dec(self.duration)
        self.start = dateutil.parser.parse(time_entry['start'])
        self.stop = dateutil.parser.parse(time_entry['stop'])
        self.billable = time_entry['billable']
        self.wid = time_entry['wid']
        self.pid = time_entry['pid']
        # self.tid = time_entry['tid']
        self.id = time_entry['id']

    @property
    def rounddown_start(self):
        """
        Round down the startup time so that it is aligned with the global roundup parameter:
            self.ROUNDUP = 15  -> :00 :15 :30 :45
            self.ROUNDUP = 30  -> :00 :30
            self.ROUNDUP = 1  -> :00
            self.ROUNDUP = 0  -> do nothing
        :param
        :return: date iso format
        """

        if self.ROUNDUP == 15:
            if 0 <= self.start.minute <= 10:
                self.start = self.start.replace(minute=0, second=0)
            elif 10 < self.start.minute <= 20:
                self.start = self.start.replace(minute=15, second=0)
            elif 20 < self.start.minute <= 40:
                self.start = self.start.replace(minute=30, second=0)
            elif 40 < self.start.minute <= 50:
                self.start = self.start.replace(minute=45, second=0)
            else:
                self.start = self.start.replace(hour=self.start.hour+1, minute=0, second=0)
        elif self.ROUNDUP == 30:
            if 0 <= self.start.minute <= 15:
                self.start = self.start.replace(minute=0, second=0)
            elif 15 < self.start.minute <= 40:
                self.start = self.start.replace(minute=30, second=0)
            elif 40 < self.start.minute <= 59:
                self.start = self.start.replace(hour=self.start.hour+1, minute=0, second=0)
        elif self.ROUNDUP == 1:
            if 0 <= self.start.minute < 6:
               self.start = self.start.replace(minute=0, second=0)
            elif 6 <= self.start.minute <= 59:
                self.start = self.start.replace(hour=self.start.hour+1, minute=0, second=0)
        #Todo recalculate duration

    @property
    def roundup_stop(self):
        """
        Round up the finish time so that it is aligned with the global roundup parameter:
            self.ROUNDUP = 15  -> :00 :15 :30 :45
            self.ROUNDUP = 30  -> :00 :30
            self.ROUNDUP = 1  -> :00
            self.ROUNDUP = 0  -> do nothing
        :param time_entry: date iso format
        :return: date iso format
        """

        if self.ROUNDUP == 15:
            if 0 < self.stop.minute <= 15:
                self.stop = self.stop.replace(minute=15, second=0)
            elif 15 < self.stop.minute <= 30:
                self.stop = self.stop.replace(minute=30, second=0)
            elif 30 < self.stop.minute <= 45:
                self.stop = self.stop.replace(minute=45, second=0)
            elif 45 < self.stop.minute <= 59:
                self.stop = self.stop.replace(hour=self.stop.hour+1, minute=0, second=0)
        elif self.ROUNDUP == 30:
            if 0 < self.stop.minute <= 30:
                self.stop = self.stop.replace(minute=30, second=0)
            elif 30 < self.stop.minute <= 59:
                self.stop = self.stop.replace(hour=self.stop.hour+1, minute=0, second=0)
        elif self.ROUNDUP == 1:
            if 0 <= self.stop.minute <= 5:
                self.stop = self.stop.replace(minute=0, second=0)
            elif 5 < self.stop.minute <= 59:
                self.stop = self.stop.replace(hour=self.stop.hour+1, minute=0, second=0)

    @property
    def calculate_duration(self):
        """
        Calculate the duration: stop - start
        :return:
        """
        self.duration = self.stop - self.start
        self.duration = self.duration.total_seconds()
        self.duration_dec = self.sec_to_hours_dec(self.duration)

    def roundup(self):
        """

        :return:
        """
        self.rounddown_start
        self.roundup_stop
        self.calculate_duration


    def sec_to_hours_dec(self,time_sec):
        """
        :return: time in hours
        """
        return time_sec/60/60


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    tt = Toggletime({u'duronly': False, u'wid': 507341, u'description': u'Test entry', \
                     u'stop': u'2015-03-18T16:55:00+00:00', u'duration': 4500, u'pid': 5503294, \
                     u'start': u'2015-03-18T15:35:00+00:00', u'at': u'2015-03-18T16:48:04+00:00', \
                     u'billable': False, u'tid': 3399821, u'id': 210886825, u'uid': 676618}, 15)
    print tt.start, tt.stop, tt.description, tt.duration, tt.ROUNDUP
    tt.rounddown_start
    tt.roundup_stop
    tt.calculate_duration

    print tt.start, tt.stop, tt.description, tt.duration, tt.ROUNDUP
    print tt.sec_to_hours_dec(tt.duration), tt.stop - tt.start

