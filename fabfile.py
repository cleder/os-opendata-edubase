#
import glob
import os
from fabric import api as fab


PROJECT_DIR = os.path.dirname(__file__)

vrt="""<OGRVRTDataSource>
    <OGRVRTLayer name="codepoint">
        <SrcDataSource>{0}</SrcDataSource>
        <GeometryType>wkbPoint</GeometryType>
        <LayerSRS>EPSG:27700</LayerSRS>
        <GeometryField encoding="PointFromColumns" x="Eastings" y="Northings"/>
    </OGRVRTLayer>
</OGRVRTDataSource>"""


def unzip_codepo():
    with fab.lcd(os.path.join(PROJECT_DIR, 'data')):
        fab.local('unzip codepo_gb.zip')

def prepend_headers():
    inpath = os.path.join(PROJECT_DIR, 'data', 'Data', 'CSV')
    outpath = os.path.join(PROJECT_DIR, 'data', 'Data', 'processed_csv')
    header =('Postcode',
            'Positional_quality_indicator',
            'Eastings',
            'Northings',
            'Country_code',
            'NHS_regional_HA_code',
            'NHS_HA_code',
            'Admin_county_code',
            'Admin_district_code',
            'Admin_ward_code',)

    if not os.path.exists(outpath):
        os.makedirs(outpath)
    for f in glob.glob(os.path.join(inpath,'*.csv')):
        print f
        with open(os.path.join(outpath, os.path.split(f)[1]), 'w') as outfile:
            with open(f, 'r') as infile:
                outfile.write(','.join(header) + '\n')
                for l in infile:
                    outfile.write(l)
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


def import_codepoint():
    first = '''ogr2ogr -nlt PROMOTE_TO_MULTI -progress -nln codepoint -skipfailures -lco PRECISION=no -f PostgreSQL PG:"dbname='osopen_data' host='localhost' port='5432'  user='osopen' password='osopen' " {0}'''
    other = '''ogr2ogr -nlt PROMOTE_TO_MULTI -progress -update -append -nln codepoint -skipfailures -lco PRECISION=no -f PostgreSQL PG:"dbname='osopen_data' host='localhost'  port='5432' user='osopen' password='osopen'" {0}'''
    path = os.path.join(PROJECT_DIR, 'data', 'Data', 'processed_csv')
    template = first
    for f in glob.glob(os.path.join(path,'*.vrt')):
        with fab.lcd(path):
            fab.local(template.format(f))
        template = other



