"""Crawl HXL to list data providers and first dates of datasets
CKAN API documentation: http://docs.ckan.org/en/latest/api/
Python CKAN library: https://github.com/ckan/ckanapi

Started by David Megginson, 2017-09-17
"""

import ckanapi, time, sys, csv

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

# Open a CSV output stream
output = csv.writer(sys.stdout)

# Iterate through all the datasets ("packages") and resources on HDX
start = 0
result_count = 999999 # just a big, big number; will reset on first search result
while start < result_count:
    result = ckan.action.package_search(fq='tags:hxl', start=start, rows=CHUNK_SIZE)
    result_count = result['count']
    print("Read {} package(s)...".format(len(result['results'])), file=sys.stderr)
    for package in result['results']:
        org = package['organization']
        created_date = package['metadata_created'][:10]
        modified_date = package['metadata_modified'][:10]
        record = hxl_providers.get(org['name'])
        if record:
            # If we've already seen this, update the count and check for earlier data
            record['count'] += 1
            if record['first_shared_date'] > created_date:
                record['first_shared_date'] = created_date
            if record['last_updated_date'] < modified_date:
                record['last_updated_date'] = modified_date
        else:
            # If we haven't seen this yet, create the record
            record = {
                'name': org['name'],
                'title': org['title'],
                'first_shared_date': created_date,
                'last_updated_date': modified_date,
                'count': 1
            }
        hxl_providers[org['name']] = record # update the record
    start += CHUNK_SIZE # next chunk, but first ...
    time.sleep(DELAY) # give HDX a short rest

# Print the output to CSV on STDOUT
output.writerow([
    'HDX org',
    'Org title',
    'Date first shared HXL',
    'Date last updated HXL',
    'Total HXL datasets',
])
for provider in hxl_providers.values():
    output.writerow([
        provider['name'],
        provider['title'],
        provider['first_shared_date'],
        provider['last_updated_date'],
        provider['count'],
    ])
        
# end
