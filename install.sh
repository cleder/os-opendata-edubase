#!/bin/bash
PROJECT_NAME=$1

DB_PASSWORD=`cat /dev/urandom | tr -dc _A-Z-a-z-0-9 | head -c 32`
echo 'localhost:5432:osopen_data:osopen:'$DB_PASSWORD > .pgpass
chown vagrant .pgpass
chmod 0600 .pgpass

# Install essential packages from apt-get
apt-get update -y
sudo apt-get upgrade -y
apt-get install -y build-essential libpq-dev ntp libffi-dev
apt-get install -y postgresql postgresql-contrib
apt-get install -y postgis postgresql-9.3-postgis-2.1
apt-get install -y gdal-bin
apt-get install -y unzip git
apt-get install -y nginx
apt-get install -y python python-dev python-virtualenv python-setuptools python-pip
pip install uwsgi

sudo -u postgres psql -c "CREATE USER osopen WITH PASSWORD '"$DB_PASSWORD"'"
sudo -u postgres createdb -O osopen osopen_data
sudo -u postgres psql -d {0} -c "CREATE EXTENSION postgis;"
sudo -u postgres psql -d {0} -c "GRANT ALL ON geometry_columns TO PUBLIC;"
sudo -u postgres psql -d {0} -c "GRANT ALL ON spatial_ref_sys TO PUBLIC;"
sudo -u postgres psql -d {0} -c "CREATE EXTENSION hstore;"

echo "export WORKON_HOME=~/Env" >> ~/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc


# fabric
mkdir $PROJECT_NAME/fabric/data
mkdir $PROJECT_NAME/fabric/data/osm
mkdir $PROJECT_NAME/fabric/venv
virtualenv $PROJECT_NAME/fabric/venv -p python2
source $PROJECT_NAME/fabric/venv/bin/activate
pip install -r $PROJECT_NAME/fabric/requirements.txt

# django
mkdir $PROJECT_NAME/django/venv
virtualenv $PROJECT_NAME/django/venv -p python2
source $PROJECT_NAME/django/venv/bin/activate
pip install -r $PROJECT_NAME/django/requirements.txt
