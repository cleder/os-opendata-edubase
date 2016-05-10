# -*- coding: utf-8 -*-

import xml.etree.ElementTree as etree

import requests
from requests_oauthlib import OAuth1Session

API_URL = 'http://api06.dev.openstreetmap.org/'


class OsmChange(object):

    """
    http://wiki.openstreetmap.org/wiki/OsmChange
    """

    def __init__(self):
        self.nodes = []
        self.ways = []
        self.multipolygons = []
        self.idx = 0

    def create_node(self, point, **kwargs):
        self.idx -= 1
        self.nodes.append(dict(id=self.idx, lat=point.x, lon=point.y, tags=dict(**kwargs))
        return self.idx

    def etree_element(self):
        root = etree.Element('osmChange')
        create_element = etree.SubElement(root, 'create')
        for node in self.nodes:
            node_element = etree.SubElement(create_element, 'node')
            node_element.set('id', node['id'])
            node_element.set('lat', node['lat'])
            node_element.set('lon', node['lon'])
            for k, v in node['tags'].items():
                tag_element = etree.SubElement(node_element, 'tag')
                tag_element.set('k', k)
                tag_element.set('v', v)
        return root

    def to_string(self):
        return etree.tostring(
                self.etree_element(),
                encoding='utf-8').decode('UTF-8')


class ChangeSet(object):

    def __init__(self, id=None, created_by=None, comment=None):
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
