# -*- coding: utf-8 -*-

import xml.etree.ElementTree as etree

import pygeoif
import requests
from requests_oauthlib import OAuth1Session

API_URL = 'http://api06.dev.openstreetmap.org/'


class OsmChange(object):

    """
    http://wiki.openstreetmap.org/wiki/OsmChange
    """

    def __init__(self, changeset):
        self.nodes = []
        self.ways = []
        self.multipolygons = []
        self.idx = 0
        self.changeset = changeset

    def create_node(self, point, **kwargs):
        self.idx -= 1
        if not isinstance(point, dict):
            point = point.__geo_interface__
        assert point['type'] == 'Point'
        assert point['coordinates']
        lon = str(point['coordinates'][0])
        lat = str(point['coordinates'][1])
        self.nodes.append(dict(id=str(self.idx), lon=lon, lat=lat, tags=dict(**kwargs)))
        return self.idx

    def create_way(self, linestring, **kwargs):
        if not isinstance(linestring, dict):
            linestring = linestring.__geo_interface__
        assert linestring['type'] == 'LineString' or linestring['type'] == 'LinearRing'
        assert linestring['coordinates']
        nodes = []
        for point in (pygeoif.Point(coord) for coord in linestring['coordinates']):
            node = self.create_node(point)
            nodes.append(node)
        self.idx -= 1
        self.ways.append(dict(id=str(self.idx), nodes=nodes, tags=dict(**kwargs)))
        return self.idx

    def create_multipolygon(self, multipolygon, **kwargs):
        if not isinstance(multipolygon, dict):
            multipolygon = multipolygon.__geo_interface__
        assert multipolygon['type'] == 'MultiPolygon' or multipolygon['type'] == 'Polygon'
        assert multipolygon['coordinates']
        if multipolygon['type'] == 'Polygon':
            polygons = [pygeoif.Polygon(multipolygon), ]
        else:
            polygons = []
            for coords in multipolygon['coordinates']:
                polygons.append(pygeoif.Polygon(coords[0], coords[1:]))
        ways = []
        for polygon in polygons:
            outer = self.create_way(polygon.exterior)
            ways.append(('outer', str(outer)))
            for way in polygon.interiors:
                inner = self.create_way(way)
                ways.append(('inner', str(inner)))
        self.idx -= 1
        self.multipolygons.append(dict(id=str(self.idx), ways=ways, tags=dict(**kwargs)))
        return self.idx


    def etree_element(self):
        def append_tags(element, tagdict):
            for k, v in tagdict.items():
                tag_element = etree.SubElement(element, 'tag')
                tag_element.set('k', k)
                tag_element.set('v', v)

        root = etree.Element('osmChange')
        create_element = etree.SubElement(root, 'create')
        for node in self.nodes:
            node_element = etree.SubElement(create_element, 'node')
            node_element.set('id', node['id'])
            node_element.set('lat', node['lat'])
            node_element.set('lon', node['lon'])
            node_element.set('changeset', str(self.changeset.id))
            append_tags(node_element, node['tags'])
        for way in self.ways:
            way_element = etree.SubElement(create_element, 'way')
            way_element.set('id', way['id'])
            way_element.set('changeset', str(self.changeset.id))
            for node in way['nodes']:
                node_element = etree.SubElement(way_element, 'nd')
                node_element.set('ref', str(node))
            append_tags(way_element, way['tags'])
        for mp in self.multipolygons:
            rel_element = etree.SubElement(create_element, 'relation')
            rel_element.set('id', mp['id'])
            rel_element.set('changeset', str(self.changeset.id))
            rel_element.set('id', mp['id'])
            for way in mp['ways']:
                member_element = etree.SubElement(rel_element, 'member')
                member_element.set('type', 'way')
                member_element.set('role', way[0])
                member_element.set('ref', way[1])
            append_tags(rel_element, {'type': 'multipolygon'})
            append_tags(rel_element, mp['tags'])
        return root

    def to_string(self):
        return etree.tostring(
                self.etree_element(),
                encoding='utf-8').decode('UTF-8')


class ChangeSet(object):

    def __init__(self, id=None, created_by='osmoapi v 0.1', comment='Changes via API'):
        self.id = id
        self.created_by = created_by
        self.comment = comment

    def etree_element(self):
        root = etree.Element('osm')
        changeset = etree.SubElement(root, 'changeset')
        created_tag = etree.SubElement(changeset, 'tag')
        created_tag.set('k', 'created_by')
        created_tag.set('v', self.created_by)
        comment_tag = etree.SubElement(changeset, 'tag')
        comment_tag.set('k', 'comment')
        comment_tag.set('v', self.comment)
        return root


    def to_string(self):
        return etree.tostring(
                self.etree_element(),
                encoding='utf-8').decode('UTF-8')


class OSMOAuthAPI(object):

    """OSM API with OAuth."""

    def __init__(self, client_key, client_secret, resource_owner_key, resource_owner_secret):
        self.session = OAuth1Session(client_key,
                                   client_secret=client_secret,
                                   resource_owner_key=resource_owner_key,
                                   resource_owner_secret=resource_owner_secret)

    def create_changeset(self, created_by, comment):
        url = '{0}api/0.6/changeset/create'.format(API_URL)
        changeset = ChangeSet(created_by=created_by, comment=comment)
        response = self.session.put(url, data=changeset.to_string())
        if response.status_code == 200:
            changeset.id = int(response.text)
            return changeset

    def close_changeset(self, changeset):
        url = '{0}api/0.6/changeset/{1}/close'.format(API_URL, changeset.id)
        response = self.session.put(url)
        if response.status_code == 200:
            return True
        else:
            return False

    def diff_upload(self, change):
        """Diff upload: POST /api/0.6/changeset/#id/upload"""
        url = '{0}api/0.6/changeset/{1}/upload'.format(API_URL, change.changeset.id)
        response = self.session.post(url, data=change.to_string())
        if response.status_code == 200:
            return response.text
        else:
            import ipdb; ipdb.set_trace()

