# todo: check if fodler exists or remove forcefully
venv/bin/python3 -m venv venv &&\
source venv/bin/activate &&\
venv/bin/pip list &&\
venv/bin/pip install -r requirements.txt