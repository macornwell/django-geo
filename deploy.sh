#!/bin/bash
rm -R dist/ django_geo_db.egg-info/
python3 setup.py sdist
twine upload dist/*
