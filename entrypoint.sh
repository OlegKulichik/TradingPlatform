#!/bin/bash
sleem 10
set -ex
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000