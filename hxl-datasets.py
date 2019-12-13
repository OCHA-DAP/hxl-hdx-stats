"""Crawl HXL to list data providers and first dates of datasets
CKAN API documentation: http://docs.ckan.org/en/latest/api/
Python CKAN library: https://github.com/ckan/ckanapi

Started by David Megginson, 2017-09-17
"""

import config # common configuration
import ckanapi, time, sys, csv

# Open a connection to HDX
ckan = ckanapi.RemoteCKAN(config.CKAN_URL)

# Open a CSV output stream
output = csv.writer(sys.stdout)

# Iterate through all the datasets ("packages") and resources on HDX
start = 0
result_count = 999999 # just a big, big number; will reset on first search result


output.writerow([
    'Dataset name',
    'Dataset title',
    'HDX org',
    'Source',
    'Date created',
    'Date updated',
])

while start < result_count:
    result = ckan.action.package_search(fq=config.SEARCH_FQ, start=start, rows=config.CHUNK_SIZE)
    result_count = result['count']
    print("Read {} package(s)...".format(len(result['results'])), file=sys.stderr)
    for package in result['results']:
        org = package['organization']
        date = package['metadata_created'][:10]
        output.writerow([
            package['name'],
            package['title'],
            package['organization']['name'],
            package['dataset_source'],
            package['metadata_created'][:10],
            package['metadata_modified'][:10],
        ])
    start += config.CHUNK_SIZE # next chunk, but first ...
    time.sleep(config.DELAY) # give HDX a short rest

# end
