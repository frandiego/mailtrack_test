
create:
	python3 -m venv venv


.ONESHELL:
.PHONY: install
install:
	( \
		source $(PWD)/venv/bin/activate; \
		pip install pandas==1.1.5; \
	)

run: create install
	$(PWD)/venv/bin/python main.py
