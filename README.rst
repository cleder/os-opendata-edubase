
Introduction
============

This application was built to enable a quick overview and import of existing
open data into OpenStreetMap_. It tries to demonstrate a possible approach
and can serve as a blueprint to build your own Application.

Getting Started
----------------

Execute the install script in this folder with `./install.sh`

Data
----

The Data is derived from:

'Code-Point' Open and 'OS Open Map - Local' from ordnancesurvey_
'All EduBase data.csv' from edubase_
'School Contact Details' from the  Scottish Government seed_

Download the data from the above sources into the data directory.

Requirements
-------------

python 2.7, ogr, gdal, postgis, shp2pgsql, ogr2ogr are required and must be installed.



Import
------

The import script is written in fabric. Excecute is as `fab init_db`





Starting the Django application
--------------------------------

Activate the virtual environment and start django::

    christian@darkstar:~/devel$ cd os-opendata/
    christian@darkstar:~/devel/os-opendata$ source bin/activate
    (os-opendata)christian@darkstar:~/devel/os-opendata$ cd osschooldata/
    (os-opendata)christian@darkstar:~/devel/os-opendata/osschooldata$ python manage.py createsuperuser
    (os-opendata)christian@darkstar:~/devel/os-opendata/osschooldata$ python manage.py runserver 0.0.0.0:8017


.. _ordnancesurvey: https://www.ordnancesurvey.co.uk/opendatadownload/products.html
.. _edubase: http://www.education.gov.uk/edubase/home.xhtml
.. _seed: http://www.gov.scot/Topics/Statistics/Browse/School-Education/Datasets/contactdetails
.. _OpenStreetMap: https://www.openstreetmap.org/#map=17/53.23383/-0.53536
