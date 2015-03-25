#!/usr/bin/python
# -*- coding: utf-8 -*-
#@author Mosab Ahmad <mosab.ahmad@gmail.com>

import requests
from urllib import urlencode
from requests.auth import HTTPBasicAuth


class TogglAPI(object):
    """A wrapper for Toggl Api"""

    def __init__(self, api_token, timezone):
        self.api_token = api_token
        self.timezone  = timezone

    def _make_url(self, section='time_entries', params={}):
        """Constructs and returns an api url to call with the section of the API to be called
        and parameters defined by key/pair values in the params dict.
        Default section is "time_entries" which evaluates to "time_entries.json"

        >>> t = TogglAPI('_SECRET_TOGGLE_API_TOKEN_')
        >>> t._make_url(section='time_entries', params = {})
        'https://www.toggl.com/api/v8/time_entries'

        >>> t = TogglAPI('_SECRET_TOGGLE_API_TOKEN_')
        >>> t._make_url(section='time_entries', params = {'start_date' : '2010-02-05T15:42:46+02:00', 'end_date' : '2010-02-12T15:42:46+02:00'})
        'https://www.toggl.com/api/v8/time_entries?start_date=2010-02-05T15%3A42%3A46%2B02%3A00%2B02%3A00&end_date=2010-02-12T15%3A42%3A46%2B02%3A00%2B02%3A00'
        """

        url = 'https://www.toggl.com/api/v8/{}'.format(section)
        if len(params) > 0:
            url = url + '?{}'.format(urlencode(params))
        return url

    def _query(self, url, method):
        """Performs the actual call to Toggl API"""

        url = url
        headers = {'content-type': 'application/json'}

        if method == 'GET':
            return requests.get(url, headers=headers, auth=HTTPBasicAuth(self.api_token, 'api_token'))
        elif method == 'POST':
            return requests.post(url, headers=headers, auth=HTTPBasicAuth(self.api_token, 'api_token'))
        else:
            raise ValueError('Undefined HTTP method "{}"'.format(method))

    ## Time Entry functions
    def get_time_entries(self, start_date='', end_date='', timezone=''):
        """Get Time Entries JSON object from Toggl"""

        url = self._make_url(section='time_entries', params={'start_date': start_date+self.timezone, 'end_date': end_date+self.timezone})
        r = self._query(url=url, method='GET')
        return r.json()

    def get_hours_tracked(self, start_date, end_date):
        """Count the total tracked hours excluding any RUNNING real time tracked time entries"""
        time_entries = self.get_time_entries(start_date=start_date.isoformat(), end_date=end_date.isoformat())

        if time_entries is None:
            return 0
        total_seconds_tracked = sum(max(entry['duration'], 0) for entry in time_entries)
        return (total_seconds_tracked / 60.0) / 60.0

    def get_tracked_entries(self, start_date, end_date):
        """Return the actual time entries in a list"""
        time_entries = self.get_time_entries(start_date=start_date.isoformat(), end_date=end_date.isoformat())
        return time_entries

    def get_time_entries_sum_per_day(self, start_date='', end_date='', timezone=''):
        """Count the total tracked hours excluding any RUNNING real time tracked time entries"""
        time_entries = self.get_time_entries(start_date=start_date.isoformat(), end_date=end_date.isoformat())

        if time_entries is None:
            return 0

class ReportAPI(object):
    """
        A wrapper for Report API v2
        https://github.com/toggl/toggl_api_docs/blob/master/reports.md
    """

    def __init__(self, api_token, timezone, workspace_id):
        self.api_token = api_token
        self.timezone  = timezone
        self.worksheet_id = workspace_id


    def _make_url(self, section='details', params={}):
        """Constructs and returns an api url to call with the section of the API to be called
        and parameters defined by key/pair values in the params dict.

        URLs:
        The reports API base URL is https://toggl.com/reports/api/v2
        Weekly report URL GET https://toggl.com/reports/api/v2/weekly
        Detailed report URL: GET https://toggl.com/reports/api/v2/details
        Summary report URL: GET https://toggl.com/reports/api/v2/summary

        Default section is "details"

        >>> t = ReportAPI('_SECRET_TOGGLE_API_TOKEN_')
        >>> t._make_url(section='details', params = {})
        'https://toggl.com/reports/api/v2/details'

        >>> t = ReportAPI('_SECRET_TOGGLE_API_TOKEN_')
        >>> t._make_url(section='details', params = {'since' : '2010-02-05T15:42:46+02:00', 'until' : '2010-02-12T15:42:46+02:00'})
        'https://toggl.com/reports/api/v2/details?start_date=2010-02-05T15%3A42%3A46%2B02%3A00%2B02%3A00&end_date=2010-02-12T15%3A42%3A46%2B02%3A00%2B02%3A00'
        """

        url = 'https://toggl.com/reports/api/v2/{}'.format(section)
        if len(params) > 0:
            url = url + '?{}'.format(urlencode(params))
        return url

    def _query(self, url, method):
        """Performs the actual call to Report API"""

        headers = {'content-type': 'application/json'}

        if method == 'GET':
            return requests.get(url, headers=headers, auth=HTTPBasicAuth(self.api_token, 'api_token'))
        elif method == 'POST':
            return requests.post(url, headers=headers, auth=HTTPBasicAuth(self.api_token, 'api_token'))
        else:
            raise ValueError('Undefined HTTP method "{}"'.format(method))

    ## Detailed Report section
    def get_detailed_report(self, since='', until='', workspace_id='', rounding='off', per_page=50):
        """Get a detailed report """

        data_list = []

        if workspace_id == '':
            workspace_id = self.worksheet_id

        url = self._make_url(section='details', params={'since': since, 'until': until,
                                                        'user_agent': 'epablo+toggletime@pabloendres.com',
                                                        'rounding': rounding, 'workspace_id': workspace_id})
        r = self._query(url=url, method='GET')
        res = r.json()

        total_count = res['total_count']
        per_page = res['per_page']
        data_list = data_list + res['data']

        # Calculate how many pages we have to get
        if total_count % per_page != 0:
            last_page = (total_count // per_page) + 1

        # print "last_page:" + str(last_page)

        if last_page > 1:
            # Get all pages
            for page in range(2, last_page+1):

                url = self._make_url(section='details', params={'since': since, 'until': until,
                                                        'user_agent': 'epablo+toggletime@pabloendres.com',
                                                        'rounding': rounding, 'workspace_id': workspace_id,
                                                        'page': page})
                r = self._query(url=url, method='GET')
                res = r.json()
                data_list = data_list + res['data']

        return data_list

if __name__ == '__main__':
    import doctest
    doctest.testmod()
