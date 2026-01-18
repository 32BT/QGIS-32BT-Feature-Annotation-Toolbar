
import json

from qgis.core import *
from qgis.PyQt.QtCore import QVariant
from .. import _qgs as QGS


################################################################################
### Shape
################################################################################
'''
Helperclass for readability and ease-of-access.
TODO: turn this into a true internal class at some point in time.
'''
class Shape(dict):
    def __init__(self, geom):
        if not geom: geom={}
        self.type = geom.get('type')
        self.data = geom.get('coordinates', [])
        super().__init__(geom)

################################################################################
### Feature
################################################################################
'''
Feature is our internal featureclass.

bool
int
str
list
dict
'''

class Feature:

    def __init__(self, geometry=None, properties=None, fid=None):
        self._fid = fid
        self.geometry = geometry
        self.properties = properties

    ########################################################################
    ### Getters & Setters
    ########################################################################
    '''
    '''
    @property
    def geometry(self):
        return self.shape

    @geometry.setter
    def geometry(self, geom):
        self.shape = Shape(geom)

    @property
    def properties(self):
        return self._data

    @properties.setter
    def properties(self, src):
        self._data = {}
        if src:
            # Need to specifically assign values so that a value of None is properly processed
            for k,v in dict(src).items(): self[k] = v

    ########################################################################

    def __str__(self):
        text = "Feature (shapetype: {})".format(self.shape.type)
        rows = [text]
        for key, value in self.properties.items():
            text = "  {:>6}: '{}'".format(key, value)
            rows += [text]
        return '\n'.join(rows)

    ########################################################################
    '''
    The crucial part of the Featureclass is that it can translate itself to
    and from the GeoJSON format for storage and exchange purposes.
    '''
    @classmethod
    def from_json(cls, text):
        data = json.loads(text)
        geom = data.get('geometry', {})
        prop = data.get('properties', {})
        return cls(geom, prop)

    def as_json(self):
        data = dict(type='Feature', geometry=self.geometry)
        if self.properties:
            data['properties'] = self.properties
        return json.dumps(data)

    ########################################################################
    '''
    Additionally, it glues to the qgis environment
    '''
    @classmethod
    def from_qgis_feature(cls, feature, p=3):
        feat = QGS.FEATURE(feature)
        geom = feat.geometry_as_dict(p)
        data = feat.properties_as_dict()
        return cls(geom, data, feature.id())

    def as_qgis_feature(self, keys=None):
        if keys is None:
            keys = self.properties.keys()
        F = QGS.FEATURE(keys)
        F.setGeometry(self.geometry)
        for f in F.fieldNames():
            F[f] = self.get(f)
        return F.feature()

    '''
    If we only need a copy of the geometry
    '''
    @classmethod
    def from_qgis_shape(cls, feature, p=3):
        feat = QGS.FEATURE(feature)
        geom = feat.geometry_as_dict(p)
        return cls(geom)

    ########################################################################
    ### Equivalence checks
    ########################################################################

    def __eq__(self, feature):
        if isinstance(feature, Feature):
            return (
            self.geometry == feature.geometry and
            self.properties == feature.properties)
        return False

    def key(self, idx):
        return self.keys()[idx]

    def keys(self):
        return list(self.properties.keys())+['shape']

    def keyDifferences(self, item, keys=None):
        if keys is None:
            keys = self.mergeKeys(item)
            return [key for key in keys if self.get(key) != item.get(key)]
        else:
            for key in keys:
                if self.get(key) != item.get(key): return True
            return False

    def mergeKeys(self, item):
        return list(dict.fromkeys(self.keys()+item.keys()))

    def mergeProperties(self, srcProperties, srcKeys=None):
        if srcKeys is None:
            srcKeys = srcFeature.property.keys()
        dstKeys = set(self.keys())
        for key in srcKeys:
            if key not in dstKeys:
                self[key] = srcFeature[key]


    ########################################################################

    def set_guid(self, key, value):
        items = [[k,v] for k,v in self.properties.items()]
        if items[0][0] == key:
            if items[0][1] == value:
                return False
            items[0][1] = value
        else:
            items = [[key, value]]+items
        self.properties = dict(items)
        return True

    ########################################################################
    '''
    Feature[key] will get/set property for key.
    Feature also allows indexing, similar to a qgis feature:
        feature[int] will get/set property at index int
    Additionally, feature is a grouped structure, so we allow "meta" keys:
        feature['shape'] will get/set geometry dict
        feature['properties'] will get/set entire properties dict

    QGIS Features have an annoyingly inconsistent use of None. Sometimes this
    will be substituted for a QVariant NULL object. A QVariant NULL object
    does not seem to play well with Python, leading to unexpected behavior.
    Since JSON also doesn't digest QVariants, we simply filter all QVariant
    objects to Python None.
    '''
    def __setitem__(self, key, val):
        # Substitute all QVariant to None
        if isinstance(val, QVariant): val = None
        # If key is index, translate index to property key
        if self._is_index_key(key):
            key = list(self.properties)[key]
        # If meta-key, set grouping attributes
        if self._is_shape_key(key):
            self.geometry = val
        elif self._is_properties_key(key):
            self.properties = val
        # Otherwise set property
        elif val is not None:
            self.properties[key] = val
        elif key in self.properties:
            del self.properties[key]

    def __getitem__(self, key):
        if self._is_index_key(key):
            key = list(self.properties)[key]
        if self._is_shape_key(key):
            return self.geometry
        if self._is_properties_key(key):
            return self.properties
        return self.properties[key]

    def get(self, key, alt=None):
        try: return self[key]
        except KeyError: return alt

    def _is_index_key(self, key):
        return (isinstance(key, int) and
        0 <= key < len(self.properties))

    def _is_shape_key(self, key):
        return (isinstance(key, str) and
        key.lower() in ('@shape', 'shape', 'geometry'))

    def _is_properties_key(self, key):
        return (isinstance(key, str) and
        key.lower() in ('@properties', 'properties'))

    ########################################################################
