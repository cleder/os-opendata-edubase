#!/bin/bash
PROJECT_NAME=$1

DB_PASSWORD=`cat /dev/urandom | tr -dc _A-Z-a-z-0-9 | head -c 32`
echo $DB_PASSWORD > DB_PASSWORD.txt
# Install essential packages from apt-get
apt-get update -y
apt-get install -y build-essential libpq-dev ntp libffi-dev
apt-get install -y postgresql postgresql-contrib
apt-get install -y postgis postgresql-9.3-postgis-2.1
apt-get install -y gdal-bin
apt-get install -y unzip git
apt-get install -y python python-dev python-virtualenv python-setuptools python-pip

echo 'local   osopen_data     osopen     trust' >> /etc/postgresql/9.3/main/pg_hba.conf

service postgresql restart

# fabric
mkdir $PROJECT_NAME/fabric/data
mkdir $PROJECT_NAME/fabric/data/osm
virtualenv venv/fabric -p python2
source venv/fabric/bin/activate
pip install -r $PROJECT_NAME/fabric/requirements.txt

# django
virtualenv venv/django -p python2
source venv/django/bin/activate
pip install -r $PROJECT_NAME/django/requirements.txt
python $PROJECT_NAME/django/manage.py migrate
