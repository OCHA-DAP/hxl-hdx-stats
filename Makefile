VENV=venv/bin/activate
OUTPUT_DIR=output

run: $(VENV)
	mkdir -pv $(OUTPUT_DIR) \
	&& . $(VENV) \
	&& echo "HXL data providers" \
	&& python3 hxl-providers.py > $(OUTPUT_DIR)/hxl-providers.csv \
	&& echo "HXL datasets" \
	&& python3 hxl-datasets.py > $(OUTPUT_DIR)/hxl-datasets.csv \
	&& ls -l $(OUTPUT_DIR)

sync:
	git fetch origin && git pull origin && git push origin

venv: $(VENV) requirements.txt
	python3 -m venv venv && . $(VENV) && pip3 install -r requirements.txt

clean:
	rm -rf venv output *.pyc
