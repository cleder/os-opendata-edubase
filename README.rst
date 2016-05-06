
Introduction
============

This application was built to enable a quick overview and import of existing
open data into OpenStreetMap_. It tries to demonstrate a possible approach
and can serve as a blueprint to build your own Application.

Getting Started
----------------

Execute the install script in this folder with `./install.sh`
I added the line::

    local   osopen_data     all                                     trust

to my `pg_hba.conf` to avoid problems with authentication

Data
----

The Data is derived from:

'Code-Point' Open and 'OS Open Map - Local' from ordnancesurvey_
'All EduBase data.csv' from edubase_
'School Contact Details' from the  Scottish Government seed_

Download the data from the above sources into the data directory.
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
    (os-opendata)christian@darkstar:~/devel/os-opendata/osschooldata$ python manage.py migrate
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
