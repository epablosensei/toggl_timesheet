Toggl Timesheet
===============

I use Toggl (www.toggl.com) to track time for my consulting work and some clients need just a simple time sheet, 
so I adapted this small little project from [toggl_target](https://github.com/mos3abof/toggl_target) to fit my needs.

It started with some tweeks, but by this version mainly the inspiration and the toggleapi.TogglAPI remain.

Installation on linux
---------------------

If you are using linux, you most probably have Python already installed on your machine.
If not, use your distro's package management system to install Python 2.7

* Download the source code from [here](https://github.com/epablosensei/toggl_timesheet/archive/master.zip)
* Navigate to the directory and create a virtual environment (recommended):

```bash
# Create virtual environment
python -m virtualenv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

> **Note:** Using a virtual environment keeps dependencies isolated and prevents conflicts with system packages. Always activate the venv before running the tool.

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
* In the command shell, create a virtual environment (recommended):

```cmd
# Install virtualenv if needed
pip install virtualenv

# Create virtual environment
python -m virtualenv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

> **Note:** Using a virtual environment keeps dependencies isolated and prevents conflicts with system packages. Always activate the venv before running the tool.

* Download toggl_target from [here](https://github.com/epablosensei/toggl_timesheet/archive/master.zip)
* Expand the downloaded zip file, copy `config.py-example` & paste it as `config.py` beside `run.py`
* In `config.py` 
** add your Toggl  API token which can be found in your Toggl account's settings.
** add your workspace_id which can be found in your Toggl account's settings.
* Change other values in `config.py` to match your case
* Run `python timesheet.py`

Container Usage (Podman/Docker)
-------------------------------

Run toggl_timesheet in a container without installing Python 2.7 on your host.

### Quick Start

```bash
# Build the image
podman build -t toggl-timesheet .
# or: docker build -t toggl-timesheet .

# Show help (no API call)
podman run --rm toggl-timesheet -h
```

### Using the Convenience Script

The `run-timesheet.sh` script auto-detects podman/docker and handles mounts:

```bash
# Show help
./run-timesheet.sh -h

# Generate timesheet for a date range
./run-timesheet.sh -s 2024-01-01 -e 2024-01-31

# Generate per-project CSVs
./run-timesheet.sh -s 2024-01-01 -e 2024-01-31 -p
```

### Manual Run

```bash
# Run with a mounted config.py (recommended)
# Note: :z flag needed for SELinux (Fedora/RHEL); safe to use elsewhere
podman run --rm \
    -v ./config.py:/app/config.py:ro,z \
    -v ./data:/app/data:z \
    toggl-timesheet -s 2024-01-01 -e 2024-01-31

# Run with environment variables instead
podman run --rm \
    -e TOGGL_API_TOKEN=your_token \
    -e TOGGL_WORKSPACE_ID=your_workspace_id \
    -v ./data:/app/data:z \
    toggl-timesheet -s 2024-01-01 -e 2024-01-31
```

### Environment Variables

When running in a container, you can configure via environment variables instead of `config.py`:

| Variable | Description | Default |
|----------|-------------|---------|
| `TOGGL_API_TOKEN` | Toggl API token | _(required)_ |
| `TOGGL_WORKSPACE_ID` | Toggl workspace ID | _(required)_ |
| `TOGGL_TIMEZONE` | Timezone offset | `+02:00` |
| `TOGGL_ROUNDUP` | Rounding precision (minutes) | `15` |
| `TOGGL_ALIGN_TIME` | Time alignment (minutes) | `15` |
| `TOGGL_DATA_DIR` | Data directory inside container | `data` |


Usage
-----

```
timeheet v0.9.1	http://www.pabloendres.com/tools#timesheet
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
     -p,         --per-project           create separate CSVs per project under each client
     -f,         --full                  export all entries to a single full.csv file


ROUNDUP = 15  -> :00 :15 :30 :45; ROUNDUP = 30  -> :00 :30; ROUNDUP= 1  -> :00, 0 -> don't round up
ALIGN = 15  -> :00 :15 :30 :45; ALIGN = 30  -> :00 :30; ALIGN= 1  -> :00, 0 -> don't round up
```


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
* [@katalyst666](https://github.com/katalyst666)


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
