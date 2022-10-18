.PHONY: docs lint

docs:
	pdoc -o docs --html --force cvgui

lint:
	pylint --disable=E1101,E0611,I1101,R0903,R0801,W0511 cvgui
	flake8 cvgui
