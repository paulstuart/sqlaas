#!/bin/bash

cd $(dirname $0)

mkdir userdata

python3 -m venv venv
. venv/bin/activate
pip install Flask
