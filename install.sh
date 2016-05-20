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

sudo apt-get install apt-transport-https ca-certificates
sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
sudo apt-get update
sudo apt-get purge lxc-docker
apt-cache policy docker-engine
sudo apt-get install linux-image-extra-$(uname -r)
sudo apt-get install apparmor
sudo apt-get install docker-engine
sudo pip install docker-compose
curl -L https://github.com/docker/machine/releases/download/v0.7.0/docker-machine-`uname -s`-`uname -m` > ~/bin/docker-machine && \
chmod +x ~/bin/docker-machine

docker-machine create -d virtualbox dev;
eval "$(docker-machine env dev)"
