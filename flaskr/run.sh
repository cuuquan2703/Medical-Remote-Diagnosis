#!/bin/bash
pip install -r requirements.txt

flask db init
flask db migrate
flask db upgrade

flask --app app run