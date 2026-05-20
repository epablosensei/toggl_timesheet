#!/usr/bin/python
# -*- coding: utf-8 -*-
# @author Pablo Endres <epablo+code@pabloendres.com>


from urllib.parse import urlencode

import requests
from requests.auth import HTTPBasicAuth


class ReportAPI(object):
    """
        A wrapper for Report API v2
        https://github.com/toggl/toggl_api_docs/blob/master/reports.md
    """

    def __init__(self, api_token: str, timezone: str, workspace_id: str) -> None:
        self.api_token = api_token
        self.timezone = timezone
        self.worksheet_id = workspace_id


    def _make_url(self, section: str = 'details', params: dict = {}):
        """Constructs and returns an api url to call with the section of the API to be called
        and parameters defined by key/pair values in the params dict.

        URLs:
        The reports API base URL is https://api.track.toggl.com/reports/api/v2
        Weekly report URL GET https://api.track.toggl.com/reports/api/v2/weekly
        Detailed report URL: GET https://api.track.toggl.com/reports/api/v2/details
        Summary report URL: GET https://api.track.toggl.com/reports/api/v2/summary

        Default section is "details"

        >>> t = ReportAPI('_SECRET_TOGGLE_API_TOKEN_')
        >>> t._make_url(section='details', params = {})
        'https://api.track.toggl.com/reports/api/v2/details'

        >>> t = ReportAPI('_SECRET_TOGGLE_API_TOKEN_')
        >>> t._make_url(section='details', params = {'since' : '2010-02-05T15:42:46+02:00', 'until' : '2010-02-12T15:42:46+02:00'})
        'https://api.track.toggl.com/reports/api/v2/details?start_date=2010-02-05T15%3A42%3A46%2B02%3A00%2B02%3A00&end_date=2010-02-12T15%3A42%3A46%2B02%3A00%2B02%3A00'
        """

        url = 'https://api.track.toggl.com/reports/api/v2/{}'.format(section)
        if len(params) > 0:
            url = url + '?{}'.format(urlencode(params))
        return url

    def _query(self, url: str, method: str) -> requests.Response:
        """Performs the actual call to Report API"""

        headers = {'content-type': 'application/json'}
        auth = HTTPBasicAuth(self.api_token, 'api_token')

        if method == 'GET':
            r = requests.get(url, headers=headers, auth=auth, timeout=30)
        elif method == 'POST':
            r = requests.post(url, headers=headers, auth=auth, timeout=30)
        else:
            raise ValueError('Undefined HTTP method "{}"'.format(method))

        r.raise_for_status()
        return r

    ## Detailed Report section
    def get_detailed_report(self, since: str = '', until: str = '', workspace_id: str = '', rounding: str = 'off', per_page: int = 50) -> list:
        """Get a detailed report """

        data_list = []
        last_page = 1   #Default is always 1

        if workspace_id == '':
            workspace_id = self.worksheet_id

        url = self._make_url(section='details', params={'since': since, 'until': until,
                                                        'user_agent': 'toggl_timesheet',
                                                        'rounding': rounding, 'workspace_id': workspace_id,
                                                        'per_page': per_page})
        r = self._query(url=url, method='GET')
        res = r.json()

        total_count = res['total_count']
        per_page = res['per_page']
        data_list = data_list + res['data']
        print("Total entries: " + str(total_count))

        # Calculate how many pages we have to get
        if total_count % per_page != 0:
            last_page = (total_count // per_page) + 1
        else:
            last_page = (total_count // per_page)

        if last_page > 1:
            # Get all pages
            for page in range(2, last_page + 1):
                url = self._make_url(section='details', params={'since': since, 'until': until,
                                                                'user_agent': 'toggl_timesheet',
                                                                'rounding': rounding, 'workspace_id': workspace_id,
                                                                'page': page})
                r = self._query(url=url, method='GET')
                res = r.json()
                data_list = data_list + res['data']

        return data_list


if __name__ == '__main__':
    import doctest

    doctest.testmod()
