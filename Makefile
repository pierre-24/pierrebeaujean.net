all: help

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  init                        to install python dependencies through pipenv"
	@echo "  sync                        update dependencies of pipenv"
	@echo "  gen                         generate pages"
	@echo "  help                        to get this help"

init:
	pipenv install --dev --ignore-pipfile

sync:
	pipenv sync --dev

gen:
	export RESUME_LANG="en"; pipenv run generate_page conf.py -r
	export RESUME_LANG="fr"; pipenv run generate_page conf.py