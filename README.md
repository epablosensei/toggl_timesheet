Toggl Timesheet
===============

I use Toggl (www.toggl.com) to track time for my consulting work and some clients need just a simple time sheet, 
so I adapted this small little project from [toggl_target](https://github.com/mos3abof/toggl_target) to fit my needs.

It started with some tweeks, but by this version mainly the inspiration and the toggleapi.TogglAPI remain.

Installation on linux
---------------------

If you are using linux, you most probably have Python already installed on your machine.
If not, use your distro's package management system to install Python 2.7

* Downloading the source code from [here](https://github.com/epablosensei/toggl_timesheet/archive/master.zip)
* navaigate to the directory and run the following command to install the required packages :

```
$ pip install -r requirements.txt
```

* Copy `config.py-example` to `config.py`
* In `config.py` 
** add your Toggl  API token which can be found in your Toggl account's settings.
** add your workspace_id which can be found in your Toggl account's settings.
* Change other values in `config.py` to match your case
* Run `python timesheet.py`

Installation on Windows
-----------------------

* If you don't have Python installed, then you must install Python 2.7 from [here](http://python.org/ftp/python/2.7.5/python-2.7.5.msi)
* Download the file
* Press the start button, select run, and run cmd.exe
* In the command shell, run these commands

```
python distribute_setup.py
easy_install pip
pip install python-dateutil requests
```

* Download toggl_target from [here](https://github.com/epablosensei/toggl_timesheet/archive/master.zip)
* Expand the downloaded zip file, copy `config.py-example` & paste it as `config.py` beside `run.py`
* In `config.py` 
** add your Toggl  API token which can be found in your Toggl account's settings.
** add your workspace_id which can be found in your Toggl account's settings.
* Change other values in `config.py` to match your case
* Run `python timesheet.py`

Usage
-----

    timeheet v-0.9	http://www.pabloendres.com/tools#timesheet
    usage:  timeheet.py [OPTION...] 
    
         -h, --help                          display this help
         -t [token], --api-token=token       Toggl API token
         -d dirname, --data-dir=dirname      directory where to store results and local database
         -r value,   --roundup=value         round up precision
         -a,         --align-time=value      Align the start - end time of each entry
         -z,         --time-zone=tz          Timezone to use. Format "+HH:MM"
         -w,         --workspace-id=id       Toogl Worskpace ID
         -s,         --start=YYYY-MM-DD      Start of the report - default: last month
         -e,         --end=YYYY-MM-DD        End of the report - default: end of last month
    
    
    ROUNDUP = 15  -> :00 :15 :30 :45; ROUNDUP = 30  -> :00 :30; ROUNDUP= 1  -> :00, 0 -> don't round up
    ALIGN = 15  -> :00 :15 :30 :45; ALIGN = 30  -> :00 :30; ALIGN= 1  -> :00, 0 -> don't round up

The output should be something like this:

    [me@dev-box toggl_timesheet]$ ./timesheet.py 
    Hi
    Checking Internet connectivity...
    
    Trying to connect to Toggl, hang on!
    
    Getting reports for entries between 2015-02-01 00:00:00 and 2015-02-28 11:59:59
    
    writing data/2015-02-Client1.csv
    writing data/2015-02-Client2.csv



Contributores
-------------

* [@epablosensei](http://www.pabloendres.com)

Support or Contact
------------------
If you have trouble using this code, your can contact info+code@pablo.com.



Bug Reports & Feature Requests
------------------------------

To report bugs, issues or feature requests please use the Issues Queue on this Github repository to make it easier for me to maintain. Please don't send those to my email.



License
-------

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
