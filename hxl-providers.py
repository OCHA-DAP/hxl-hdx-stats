"""Crawl HXL to list data providers and first dates of datasets
CKAN API documentation: http://docs.ckan.org/en/latest/api/
Python CKAN library: https://github.com/ckan/ckanapi

Started by David Megginson, 2017-09-17
"""

import ckanapi, time, sys
from pprint import pprint

DELAY = 2
"""Time delay in seconds between datasets, to give HDX a break."""

CHUNK_SIZE=100
"""Number of datasets to read at once"""

CKAN_URL = 'https://data.humdata.org'
"""Base URL for the CKAN instance."""

hxl_providers = {}
"""List of HXL data providers, the number of datasets, and the earliest date."""

# Open a connection to HDX
ckan = ckanapi.RemoteCKAN(CKAN_URL)

# Iterate through all the datasets ("packages") and resources on HDX
start = 0
result_count = 999999
while start < result_count:
    result = ckan.action.package_search(fq='tags:hxl', start=start, rows=CHUNK_SIZE)
    result_count = result['count']
    print("Read {} package(s)...".format(len(result['results'])), file=sys.stderr)
    for package in result['results']:
        org = package['organization']
        date = package['metadata_created']
        record = hxl_providers.get(org['name'])
        if record:
            record['count'] += 1
            if record['date'] > date:
                record['date'] = date
        else:
            record = {
                'name': org['name'],
                'title': org['title'],
                'date': date,
                'count': 1
            }
        hxl_providers[org['name']] = record
    start += CHUNK_SIZE
    time.sleep(DELAY) # give HDX a short rest

pprint(hxl_providers)

# end
