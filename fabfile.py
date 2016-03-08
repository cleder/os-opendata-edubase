#
import csv
import glob
import os
from fabric import api as fab


PROJECT_DIR = os.path.dirname(__file__)

vrt="""<OGRVRTDataSource>
    <OGRVRTLayer name="codepoint">
        <SrcDataSource>{0}</SrcDataSource>
        <GeometryType>wkbPoint</GeometryType>
        <LayerSRS>EPSG:27700</LayerSRS>
        <GeometryField encoding="PointFromColumns" x="eastings" y="northings"/>
    </OGRVRTLayer>
</OGRVRTDataSource>"""


def unzip_codepo():
    with fab.lcd(os.path.join(PROJECT_DIR, 'data')):
        fab.local('unzip codepo_gb.zip')

def prepend_headers():
    inpath = os.path.join(PROJECT_DIR, 'data', 'Data', 'CSV')
    outpath = os.path.join(PROJECT_DIR, 'data', 'Data', 'processed_csv')
    header =['postcode',
            'positional_quality_indicator',
            'eastings"',
            'northings',
            'country_code',
            'nhs_regional_ha_code',
            'nhs_ha_code',
            'admin_county_code',
            'admin_district_code',
            'admin_ward_code',]

    if not os.path.exists(outpath):
        os.makedirs(outpath)
    for f in glob.glob(os.path.join(inpath,'*.csv')):
        print f
        with open(os.path.join(outpath, os.path.split(f)[1]), 'w') as outfile:
            with open(f, 'r') as infile:
                writer = csv.writer(outfile)
                writer.writerow(header)
                reader = csv.reader(infile)
                for row in reader:
                    writer.writerow(row)
        csvname=os.path.split(f)[1]
        vofname=csvname.split('.')[0] + '.vrt'
        vrt_name = os.path.join(outpath, vofname)
        with open(vrt_name, 'w') as vrtfile:
            vrtfile.write(vrt.format(vrt_name))

def create_db():
    with fab.settings(warn_only=True):
        fab.local('sudo -u postgres createuser -P osopen')
        fab.local('sudo -u postgres createdb -O osopen osopen_data')
        fab.local('sudo -u postgres psql -d osopen_data -c "CREATE EXTENSION postgis;"')
        fab.local('sudo -u postgres psql -d osopen_data -c "GRANT ALL ON geometry_columns TO PUBLIC;"')
        fab.local('sudo -u postgres psql -d osopen_data -c "GRANT ALL ON spatial_ref_sys TO PUBLIC;"')


def ogr2ogr_import_codepoint():
    first = '''ogr2ogr -nlt PROMOTE_TO_MULTI -progress -nln codepoint -skipfailures -lco PRECISION=no -f PostgreSQL PG:"dbname='osopen_data' host='localhost' port='5432'  user='osopen' password='osopen' " {0}'''
    other = '''ogr2ogr -nlt PROMOTE_TO_MULTI -progress -update -append -nln codepoint -skipfailures -lco PRECISION=no -f PostgreSQL PG:"dbname='osopen_data' host='localhost'  port='5432' user='osopen' password='osopen'" {0}'''
    path = os.path.join(PROJECT_DIR, 'data', 'Data', 'processed_csv')
    template = first
    for f in glob.glob(os.path.join(path,'*.vrt')):
        with fab.lcd(path):
            fab.local(template.format(f))
        template = other

def sql_import():
    """
DROP TABLE IF EXISTS postcodes_raw;

CREATE TABLE postcodes_raw (
  postcode character varying(10),
  easting character varying(7),
  northing character varying(7)
);

\copy postcodes_raw from pstdin delimiter ',' csv;

DROP TABLE IF EXISTS postcodes;

SELECT
  postcode,
  ST_TRANSFORM(ST_GEOMFROMEWKT('SRID=27700;POINT(' || easting || ' ' || northing || ')'), 4326)::GEOGRAPHY(Point, 4326) AS location
INTO
  postcodes
FROM
  postcodes_raw;

CREATE INDEX postcodes_geog_idx ON postcodes USING GIST(location);

DROP TABLE postcodes_raw;
    """
    fab.local('psql -d osopen_data -U osopen -c "DROP TABLE IF EXISTS postcodes_raw;"')
    fab.local('''psql -d osopen_data -U osopen -c "CREATE TABLE postcodes_raw (
            Postcode character varying(10),
            Positional_quality_indicator character varying(50),
            Eastings character varying(10),
            Northings character varying(10),
            Country_code character varying(50),
            NHS_regional_HA_code character varying(50),
            NHS_HA_code character varying(50),
            Admin_county_code character varying(50),
            Admin_district_code character varying(50),
            Admin_ward_code character varying(50));"
            ''')
    path = os.path.join(PROJECT_DIR, 'data', 'Data', 'processed_csv')
    for f in glob.glob(os.path.join(path,'*.csv')):
        fab.local('''psql -d osopen_data -U osopen -c "\copy postcodes_raw from {0} WITH (FORMAT CSV, HEADER, DELIMITER ',');"'''.format(f))
    fab.local('psql -d osopen_data -U osopen -c "DROP TABLE IF EXISTS postcodes;"')
    fab.local('''psql -d osopen_data -U osopen -c "SELECT
        postcode,
        ST_TRANSFORM(ST_GEOMFROMEWKT('SRID=27700;POINT(' || eastings || ' ' || northings || ')'), 4326)::GEOGRAPHY(Point, 4326) AS location
        INTO postcodes FROM postcodes_raw;"''')
    fab.local('psql -d osopen_data -U osopen -c "CREATE INDEX postcodes_geog_idx ON postcodes USING GIST(location);"')
    fab.local('psql -d osopen_data -U osopen -c "DROP TABLE postcodes_raw;"')

