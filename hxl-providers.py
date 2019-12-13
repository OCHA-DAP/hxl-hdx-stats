"""Crawl HXL to list data providers and first dates of datasets
CKAN API documentation: http://docs.ckan.org/en/latest/api/
Python CKAN library: https://github.com/ckan/ckanapi

Started by David Megginson, 2017-09-17
"""

import config # standard configuration
import ckanapi, time, sys, csv

hxl_providers = {}
"""List of HXL data providers, the number of datasets, and the earliest date."""

# Open a connection to HDX
ckan = ckanapi.RemoteCKAN(config.CKAN_URL)

# Open a CSV output stream
output = csv.writer(sys.stdout)

# Iterate through all the datasets ("packages") and resources on HDX
start = 0
result_count = 999999 # just a big, big number; will reset on first search result
while start < result_count:
    result = ckan.action.package_search(fq=config.SEARCH_FQ, start=start, rows=config.CHUNK_SIZE)
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
    start += config.CHUNK_SIZE # next chunk, but first ...
    time.sleep(config.DELAY) # give HDX a short rest

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
