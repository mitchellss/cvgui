.PHONY: docs lint

docs:
	pdoc -o docs --html --force cvgui

lint:
	pylint --disable=R0903,I1101,E1101,E0611,W0511 cvgui
	flake8 cvgui
