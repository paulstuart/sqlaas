#!/bin/bash

export FLASK_APP=${FLASK_APP:-routes.py}

flask run
