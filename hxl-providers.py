"""Crawl HXL to list data providers and first dates of datasets
CKAN API documentation: http://docs.ckan.org/en/latest/api/
Python CKAN library: https://github.com/ckan/ckanapi

Started by David Megginson, 2017-09-17
"""

import ckanapi, time

DELAY = 5
"""Time delay in seconds between datasets, to give HDX a break."""

CKAN_URL = 'https://data.humdata.org'
"""Base URL for the CKAN instance."""

# Open a connection to HDX
ckan = ckanapi.RemoteCKAN(CKAN_URL)

# Iterate through all the datasets ("packages") and resources on HDX
for package_id in ckan.action.package_list():
    package = ckan.action.package_show(id=package_id)
    print("Package: {}".format(package['title']))
    for resource in package['resources']:
        print("  Resource: {}".format(resource['name']))
        print("    URL: {}".format(resource['url']))
    print("")
    time.sleep(DELAY) # give HDX a short rest

# end
