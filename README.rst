
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

The import script is written in fabric. Excecute is as `fab init_db`.
If all goes well you can now connect to the database and inpect the
data.


Starting the Django application
--------------------------------

Activate the virtual environment and start django::

    christian@darkstar:~/devel$ cd os-opendata/
    christian@darkstar:~/devel/os-opendata$ source bin/activate
    (os-opendata)christian@darkstar:~/devel/os-opendata$ cd osschooldata/
    (os-opendata)christian@darkstar:~/devel/os-opendata/osschooldata$ python manage.py createsuperuser
    (os-opendata)christian@darkstar:~/devel/os-opendata/osschooldata$ python manage.py runserver 0.0.0.0:8017

Goto `http://localhost:8017/` in your browser.

Click on login to start
.. image:: https://raw.github.com/cleder/os-opendata-edubase/master/docs/login.png
Once authenticated start by clicking on *start*
.. image:: https://raw.github.com/cleder/os-opendata-edubase/master/docs/logged_in.png
If data from OSM is available it will display as an amber polygon, The Data from
Ordnancesurvey is displayed as a blue polygon and the data from seed/edubase as
a blue marker. Below the map details of this data is displayed.
.. image:: https://raw.github.com/cleder/os-opendata-edubase/master/docs/assign.png
If there is no openstreetmap data only the Ordnancesurvey data is displayed.
.. image:: https://raw.github.com/cleder/os-opendata-edubase/master/docs/assign-nosm.png

TODO
----

Add OpenStreetMap_ api so that one can easily submit data from this application to
OpenStreetMap without having to copy and paste.


.. _ordnancesurvey: https://www.ordnancesurvey.co.uk/opendatadownload/products.html
.. _edubase: http://www.education.gov.uk/edubase/home.xhtml
.. _seed: http://www.gov.scot/Topics/Statistics/Browse/School-Education/Datasets/contactdetails
.. _OpenStreetMap: https://www.openstreetmap.org/#map=17/53.23383/-0.53536
