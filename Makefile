.PHONY: docs lint

docs:
	pdoc cvgui -o ./docs

lint:
	pylint --disable=R0903,I1101,E1101,E0611,W0511 cvgui
	flake8 cvgui
	pydocstyle cvgui
