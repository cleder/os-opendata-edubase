# -*- coding: utf-8 -*-

import json
import requests

from django.contrib.gis import geos

base_url = 'http://api.ratings.food.gov.uk/'
headers = {
    'x-api-version': '2',
    'Accept': 'application/json',
}

FIELDS = {
    'fhrs_id': 'FHRSID',
    'business_name': 'BusinessName',
    'business_type': 'BusinessType',
    'address_line1': 'AddressLine1',
    'address_line1': 'AddressLine2',
    'address_line1': 'AddressLine3',
    'address_line1': 'AddressLine4',
    'postcode': 'PostCode',
}


def get_establishments(local_authority_id=None):
    """Get establisments for a local Authority Id."""
    params = {}
    if local_authority_id:
        params['localAuthorityId'] = local_authority_id
    url = base_url + 'Establishments'
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()['establishments']


def to_geometry(geocode):
    """Convert the longitude and latitude into a point."""
    lat = geocode.get('latitude', 0)
    lon = geocode.get('longitude', 0)
    if lat or lon:
        import ipdb; ipdb.set_trace()
        return geos.Point(float(lon), float(lat))


def parse_establishment(establishment):
    point = None
    if establishment.get('geocode', None):
        point = to_geometry(establishment['geocode'])
    simplified = {}
    for f in FIELDS.keys():
        simplified[f] = establishment[FIELDS[f]]
    simplified['location'] = point
    return simplified



