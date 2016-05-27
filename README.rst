
Introduction
============

This application was built to enable a quick overview and import of existing
open data into OpenStreetMap_. It tries to demonstrate a possible approach
and can serve as a blueprint to build your own Application.

Getting Started
----------------

Clone this repository with `git clone https://github.com/cleder/os-opendata-edubase.git`

`Download Vagrant<https://www.vagrantup.com/downloads.html>`_ and
`install it<https://www.vagrantup.com/docs/installation/>`_ on your machine.

Change into the cloned directory and execute `vagrant up`

This will build the virtual machine and set up the database.


Data
----

The Data is derived from:

'Code-Point' Open and 'OS Open Map - Local' from ordnancesurvey_
'All EduBase data.csv' from edubase_
'School Contact Details' from the  Scottish Government seed_

From https://www.ordnancesurvey.co.uk/opendatadownload/products.html
you have to download the
**`OS Open Map - Local`** (all squares) and **`Code-Point Open`** Products.

You will also need the csv files from EduBase and seed for the schooldata
**`All EduBase data.csv`** from http://www.education.gov.uk/edubase/home.xhtml
and **`School contact details`** from
http://www.gov.scot/Topics/Statistics/Browse/School-Education/Datasets/contactdetails

The latter is in excel format and has to be converted into csv before
using it.
Remove the first 5 Rows so that the column titles ar in the top row.
The headers must be:
'SeedCode',
'LA Name',
'Centre Type',
'School Name',
'Address 1',
'Address 2',
'Address 3',
'Post code',
'E-mail',
'Phone',
'Primary_school',
'Secondary',
'Special',
'Primary roll',
'Secondary roll',
'Special roll',
'Primary1',
'Secondary1',
'Special1',
'Denomination'
so rename them accordingly and remove the columns (`6-Fold Urban/rural measure(1)` and following)
not included here.

Put the data from the above sources into the `fabric/data` directory.
It should have these files in it::

    seeddata2015.csv
    edubasealldata20160308.csv
    codepo_gb.zip
    opmplc_essh_hp.zip
    opmplc_essh_ht.zip
    opmplc_essh_hu.zip
    opmplc_essh_hw.zip
    opmplc_essh_hx.zip
    opmplc_essh_hy.zip
    opmplc_essh_hz.zip
    opmplc_essh_na.zip
    opmplc_essh_nb.zip
    opmplc_essh_nc.zip
    opmplc_essh_nd.zip
    opmplc_essh_nf.zip
    opmplc_essh_ng.zip
    opmplc_essh_nh.zip
    opmplc_essh_nj.zip
    opmplc_essh_nk.zip
    opmplc_essh_nl.zip
    opmplc_essh_nm.zip
    opmplc_essh_nn.zip
    opmplc_essh_no.zip
    opmplc_essh_nr.zip
    opmplc_essh_ns.zip
    opmplc_essh_nt.zip
    opmplc_essh_nu.zip
    opmplc_essh_nw.zip
    opmplc_essh_nx.zip
    opmplc_essh_ny.zip
    opmplc_essh_nz.zip
    opmplc_essh_ov.zip
    opmplc_essh_sd.zip
    opmplc_essh_se.zip
    opmplc_essh_sh.zip
    opmplc_essh_sj.zip
    opmplc_essh_sk.zip
    opmplc_essh_sm.zip
    opmplc_essh_sn.zip
    opmplc_essh_so.zip
    opmplc_essh_sp.zip
    opmplc_essh_sr.zip
    opmplc_essh_st.zip
    opmplc_essh_su.zip
    opmplc_essh_sv.zip
    opmplc_essh_sw.zip
    opmplc_essh_sx.zip
    opmplc_essh_sy.zip
    opmplc_essh_sz.zip
    opmplc_essh_ta.zip
    opmplc_essh_tf.zip
    opmplc_essh_tg.zip
    opmplc_essh_tl.zip
    opmplc_essh_tm.zip
    opmplc_essh_tq.zip
    opmplc_essh_tr.zip
    opmplc_essh_tv.zip
    oprvrs_essh_gb.zip


Import
------

Connect to your vagrant box with `vagrant ssh`.

Inside the box execute the commands::

    cd os-edu-server/fabric/
    source venv/bin/activate
    fab init_db
    exit


If all goes well you can now connect to the database and inpect the
data. Leave the Box with



Starting the Django application
--------------------------------

Connect to your vagrant box with `vagrant ssh`.


Activate the virtual environment and start django::

    vagrant@vagrant-ubuntu-trusty-64:~$ cd os-edu-server/django/
    vagrant@vagrant-ubuntu-trusty-64:~/os-edu-server/django$ source venv/bin/activate
    (venv)vagrant@vagrant-ubuntu-trusty-64:~/os-edu-server/django$ python manage.py migrate
    (venv)vagrant@vagrant-ubuntu-trusty-64:~/os-edu-server/django$ python manage.py createsuperuser
    (venv)vagrant@vagrant-ubuntu-trusty-64:~/os-edu-server/django$ python manage.py runserver 0.0.0.0:8000


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

If there is no data from edubase or seed (i.e. outdated OS-Open data - school is closed):

.. image:: https://raw.github.com/cleder/os-opendata-edubase/master/docs/assign-no-school.png

The below image indicates that the school that once existed here was closed:

.. image:: https://raw.github.com/cleder/os-opendata-edubase/master/docs/assign-osm-no-edudata.png

You can switch between OpenStreetMap

.. image:: https://raw.github.com/cleder/os-opendata-edubase/master/docs/bg-osm.png

and satellite imagery.

.. image:: https://raw.github.com/cleder/os-opendata-edubase/master/docs/bg-sat.png


TODO
----

.. _ordnancesurvey: https://www.ordnancesurvey.co.uk/opendatadownload/products.html
.. _edubase: http://www.education.gov.uk/edubase/home.xhtml
.. _seed: http://www.gov.scot/Topics/Statistics/Browse/School-Education/Datasets/contactdetails
.. _OpenStreetMap: https://www.openstreetmap.org/
