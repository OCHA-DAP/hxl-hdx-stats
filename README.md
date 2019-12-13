Collect HXL stats from HDX
==========================

# Requirements:

- Python3
- ckanapi package

# Usage:

    $ pip install -r requirements.txt
    $ cp config.py.TEMPLATE config.py # edit if desired
    $ python3 hxl-providers.py > providers.csv
    $ python3 hxl-datasets.py > datasets.csv

# Web links

- http://hxlstandard.org
- https://data.humdata.org

# Unlicense

This software was written by David Megginson, and is released into the Public Domain. Feel free to adopt it for use with other CKAN deployments (or anything else).