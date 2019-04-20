#!/bin/bash

[[ -z $VIRTUAL_ENV ]] && . ./venv/bin/activate

export FLASK_APP=${FLASK_APP:-routes.py}

flask run
