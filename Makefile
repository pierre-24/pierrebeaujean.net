all: help

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  init                        to install python dependencies"
	@echo "  gen                         generate pages"
	@echo "  help                        to get this help"

init:
	pip-sync

lint:
	flake8 static_website gen.py --max-line-length=120 --ignore=N802

gen:
	python3 ./gen.py
