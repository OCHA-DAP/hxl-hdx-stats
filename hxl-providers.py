"""Crawl HXL to list data providers and first dates of datasets
CKAN API documentation: http://docs.ckan.org/en/latest/api/
Python CKAN library: https://github.com/ckan/ckanapi

Started by David Megginson, 2017-09-17
"""

import config # standard configuration
import ckancrawler, csv, logging, sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("hxl-providers")
"""Set up a logger"""

hxl_providers = {}
"""List of HXL data providers, the number of datasets, and the earliest date."""

# Open a connection to HDX
crawler = ckancrawler.Crawler(config.CKAN_URL, delay=0, user_agent=config.USER_AGENT)

# Iterate through all the datasets ("packages") on HDX tagged as HXL
for i, package in enumerate(crawler.packages(fq=config.SEARCH_FQ)):
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

    # let the user know how it's going
    if (i+1) % 100 == 0:
        logger.info("Processed %d datasets, %d unique orgs...", i+1, len(hxl_providers))

else:
    # print the final results
    logger.info("Total: %d datasets, %d unique orgs.", i+1, len(hxl_providers))

# Print the output to CSV on STDOUT
# Open a CSV output stream
output = csv.writer(sys.stdout)

output.writerow([
    'HDX org',
    'Org title',
    'Date first shared HXL',
    'Date last updated HXL',
    'Total HXL datasets',
])

# write all the orgs, in inverse order of the creation date of their earliest HXL dataset
for provider in sorted(hxl_providers.values(), reverse=True, key=lambda a: a['first_shared_date']):
    output.writerow([
        provider['name'],
        provider['title'],
        provider['first_shared_date'],
        provider['last_updated_date'],
        provider['count'],
    ])


sys.exit(0)
        
# end
