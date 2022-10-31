Collect HXL stats from HDX
==========================

Python scripts to collect information from the [Humanitarian Data Exchange](https://data.humdata.org) (HDX) about the usage of the [Humanitarian Exchange Language](https://hxlstandard.org) (HXL).

The output appears in the following HXLated CSV files:

- ``output/hxl-providers.csv`` List of organisations sharing HXLated data on HDX, along with the first date shared and the most-recent date updated.
- ``output/hxl-datasets.csv`` List of HXLated datasets on HDX, along with the date created and most-recent date updated

This information appears in the HDX datasets [HXL data on HDX](https://data.humdata.org/dataset/hxl-data-on-hdx), updated weekly.

## Requirements

- Python3
- make

## Usage

Generate reports:

    $ make

Regenerate reports:

    $ make clean reports

Update Python packages:

    $ make real-clean

Push commits to GitHub:

    $ make sync

## Web links

- http://hxlstandard.org
- https://data.humdata.org

## Unlicense

This software was written by David Megginson, and is released into the Public Domain. Feel free to adopt it for use with other CKAN deployments (or anything else).