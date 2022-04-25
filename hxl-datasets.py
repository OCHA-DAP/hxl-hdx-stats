"""Crawl HXL to list data providers and first dates of datasets
CKAN API documentation: http://docs.ckan.org/en/latest/api/
Python CKAN library: https://github.com/ckan/ckanapi

Started by David Megginson, 2017-09-17
"""

import config # common configuration
import ckancrawler, csv, logging, sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("hxl-datasets")
"""Set up a logger"""

# Open a connection to HDX
crawler = ckancrawler.Crawler(config.CKAN_URL, delay=0, user_agent=config.USER_AGENT)

# Open a CSV output stream
output = csv.writer(sys.stdout)

output.writerow([
    'Dataset name',
    'Dataset title',
    'HDX org',
    'Source',
    'Date created',
    'Date updated',
])

output.writerow([
    '#item +dataset +code',
    '#item +dataset +name',
    '#org +code',
    '#meta +source',
    '#date +start',
    '#date +updated',
])

# Iterate through all the datasets ("packages") on HDX tagged as HXL
for i, package in enumerate(crawler.packages(fq=config.SEARCH_FQ, sort="metadata_created desc")):
    
    output.writerow([
        package['name'],
        package['title'],
        package['organization']['name'],
        package['dataset_source'],
        package['metadata_created'][:10],
        package['metadata_modified'][:10],
    ])

    # let the user know how it's going
    if (i+1) % 100 == 0:
        logger.info("Processed %d datasets...", i+1)

else:
    # print the final results
    logger.info("Total: %d datasets.", i+1)

sys.exit(0)

# end
