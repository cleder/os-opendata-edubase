#!/bin/bash
virtualenv .
mkdir fabric/data
mkdir fabric/data/osm
virtualenv fabric -p python2
virtualenv django -p python3
source django/bin/activate
pip install -r django/requirements.txt
source fabric/bin/activate
pip install -r fabric/requirements.txt
