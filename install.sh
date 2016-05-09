#!/bin/bash
virtualenv .
mkdir data
mkdir data/osm
source bin/activate
pip install -r requirements.txt

