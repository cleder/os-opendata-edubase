# -*- coding: utf-8 -*-
import unittest

from pygeoif import geometry

from . import osmoapi


class OsmChangeTest(unittest.TestCase):

    def test_create_node_from_point(self):
        point = geometry.Point(0,1)
        changeset = osmoapi.ChangeSet(id=1)
        change = osmoapi.OsmChange(changeset)
        change.create_node(point)
        expected = '<osmChange><create><node changeset="1" id="-1" lat="1.0" lon="0.0" /></create></osmChange>'
        assert change.to_string() == expected

    def test_create_node_from_dict(self):
        point = geometry.Point(0,2)
        changeset = osmoapi.ChangeSet(id=2)
        change = osmoapi.OsmChange(changeset)
        change.create_node(point.__geo_interface__)
        expected = '<osmChange><create><node changeset="2" id="-1" lat="2.0" lon="0.0" /></create></osmChange>'
        assert change.to_string() == expected

    def test_create_node_extra_tags(self):
        point = geometry.Point(0,1)
        changeset = osmoapi.ChangeSet(id=3)
        change = osmoapi.OsmChange(changeset)
        change.create_node(point, email='christian.ledermann@gmail.com', author='Christian Ledermann')
        assert 'k="email"' in change.to_string()
        assert 'v="christian.ledermann@gmail.com"' in change.to_string()
        assert 'k="author"' in change.to_string()
        assert 'v="Christian Ledermann"' in change.to_string()
        assert 'changeset="3"' in change.to_string()

    def test_create_way(self):
        linestr = geometry.LineString([(0, 0), (1, 1)])
        changeset = osmoapi.ChangeSet(id=4)
        change = osmoapi.OsmChange(changeset)
        change.create_way(linestr)
        assert '<node changeset="4" id="-1" lat="0.0" lon="0.0" />' in change.to_string()
        assert '<node changeset="4" id="-2" lat="1.0" lon="1.0" />' in change.to_string()
        assert '<way changeset="4" id="-3"><nd ref="-1" /><nd ref="-2" /></way>' in change.to_string()

    def test_create_way_with_tags(self):
        linestr = geometry.LineString([(0, 0), (1, 1)])
        changeset = osmoapi.ChangeSet(id=5)
        change = osmoapi.OsmChange(changeset)
        change.create_way(linestr, creator='Christian')
        assert '<tag k="creator" v="Christian" /></way>' in change.to_string()

    def test_create_multipolygon(self):
        p = geometry.Polygon([(0, 0), (1, 1), (1, 0), (0, 0)])
        e = [(0, 0), (0, 2), (2, 2), (2, 0), (0, 0)]
        i = [(1, 0), (0.5, 0.5), (1, 1), (1.5, 0.5), (1, 0)]
        ph1 = geometry.Polygon(e, [i])
        mp = geometry.MultiPolygon([p, ph1])
        changeset = osmoapi.ChangeSet(id=6)
        change = osmoapi.OsmChange(changeset)
        change.create_multipolygon(mp)
        print change.to_string()
        assert '<relation changeset="6" id="-18">' in change.to_string()
        assert '<tag k="type" v="multipolygon" />' in change.to_string()
        assert '<member ref="-5" role="outer" type="way" />' in change.to_string()
        assert '<member ref="-17" role="inner" type="way" />' in change.to_string()


class ChangeSetTest(unittest.TestCase):

    def test_changeset_create(self):
        changeset = osmoapi.ChangeSet(created_by='me', comment='A Comment')
        assert changeset.to_string().startswith('<osm>')
        assert '<tag' in changeset.to_string()
        assert 'k="created_by"' in changeset.to_string()
        assert 'k="comment"' in changeset.to_string()
        assert 'v="me"' in changeset.to_string()
        assert 'v="A Comment"' in changeset.to_string()
