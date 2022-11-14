################################################################
# Makefile to generate HXL stats from HDX data.humdata.org
#
# Before running, copy config.py.TEMPLATE to config.py
# and update any values.
#
# Requires Python3
#
# Generate reports: make reports
#
# Regenerate reports: make clean reports
#
# Push commits to GitHub: make sync
########################################################################

VENV=venv/bin/activate
OUTPUT_DIR=output
HXL_PROVIDERS=$(OUTPUT_DIR)/hxl-providers.csv
HXL_DATASETS=$(OUTPUT_DIR)/hxl-datasets.csv

all: reports

reports: $(HXL_PROVIDERS) $(HXL_DATASETS)

refresh: clean reports

$(HXL_PROVIDERS): $(VENV) config.py hxl-providers.py
	. $(VENV) && mkdir -pv $(OUTPUT_DIR) \
	&& python3 hxl-providers.py > $@

$(HXL_DATASETS): $(VENV) config.py hxl-datasets.py
	. $(VENV) && mkdir -pv $(OUTPUT_DIR) \
	&& python3 hxl-datasets.py > $@

$(VENV): requirements.txt
	python3 -m venv venv && . $(VENV) && pip3 install -r requirements.txt

venv: $(VENV)

sync:
	git fetch origin && git pull origin && git push origin

clean:
	rm -rvf $(HXL_PROVIDERS) $(HXL_DATASETS)

real-clean: clean
	rm -rvf venv *.pyc $(OUTPUT_DIR)

# end
