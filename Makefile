FILE_ACTIVE='./md/index.md'
PROJECT_PATH='.'

prepare : venv/bin/flask

run-and-watch :
	gnome-terminal -e './tools/run-and-watch.sh' --geometry=140x45
run : run-prereqs
	FLASK_APP=flaskmarkdown FLASK_DEBUG=TRUE venv/bin/flask run
watch :
	./tools/watch.sh
venv/bin/flask : venv/bin/python3
	venv/bin/python3 -m pip install -r ./requirements.txt
venv/bin/python3 :
	python3 -m venv venv
open-new-tab:
	./tools/open-new-tab.sh $(FILE_ACTIVE) $(PROJECT_PATH)
clean :
	rm -r venv

.PHONY : run-and-watch run-prereqs run watch clean
