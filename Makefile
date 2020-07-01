all: help

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  init                        to install python dependencies"
	@echo "  gen                         generate pages"
	@echo "  help                        to get this help"

init:
	pip-sync

gen:
	export RESUME_LANG="en"; generate_page conf.py -r
	export RESUME_LANG="fr"; generate_page conf.py
