#!/bin/bash

[[ -z $VIRTUAL_ENV ]] && . ./venv/bin/activate

export FLASK_DEBUG=1
export FLASK_APP=${FLASK_APP:-routes.py}

flask run
