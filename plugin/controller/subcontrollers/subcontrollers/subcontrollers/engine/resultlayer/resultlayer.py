################################################################################
### UTC relative local time (timezone-aware datetime)
################################################################################
'''
Result always includes a timestamp. If timestamp slot is empty, it will be set.
'''
import datetime

def local_time():
    return datetime.datetime.now().astimezone()
def local_time_as_str():
    return local_time().isoformat(timespec='milliseconds')

################################################################################
'''
Local default style files are available in the plugin folder in the same
directory as this file.
'''
import os

def _getcwd():
    return os.path.split(__file__)[0]

def _itempath(name):
    return os.path.join(_getcwd(), name)

################################################################################

from qgis.core import *
from . import qgs
from .layer import Layer
from .tablelayer import TableLayer
from ..database.table import FeatureTable
################################################################################
### Sentinel
################################################################################
'''
In order to prepopulate our ResultLayers with features, we use a sentinelobject
to listen for layer-load signals.
'''
'''
class Sentinel:
    def __init__(self):
        for layer in QgsProject.instance().mapLayers().values():
            self.layerWasAdded(layer)
        QgsProject.instance().layerWasAdded.connect(self.layerWasAdded)

    def layerWasAdded(self, layer):
        if ResultLayer.validate(layer):
            if not layer.hasFeatures():
                TableLayer(layer).refresh()


_sentinel = Sentinel()
'''
################################################################################
### ResultLayer
################################################################################
'''
By default a resultlayer contains:
    - geometry
    - guid
    - date

TODO:
    determine additional/dynamic defaults like
    - status (new, ..., archived)
    - result (label, ...)
    - info/comment
    determine lock-states
    - locked

    Note that a locked state can occur in combination with any status,
    and status is also a kind of label, usually an automated label.
'''


class ResultLayer(TableLayer):

    @classmethod
    def get_qgis_layer(cls, tablePath, srcLayer, srcField):
        layer = cls.find_qgis_layer(tablePath)
        if layer is None:
            layer = cls.make_qgis_layer(tablePath, srcLayer, srcField)
        return layer


    @classmethod
    def make_qgis_layer(cls, tablePath, srcLayer, srcField):
        path, tablename = os.path.split(tablePath)
        path, sessionName = os.path.split(path)
        path, layerName = os.path.split(path)
        name = layerName+'_'+sessionName
        layer = cls.create_qgis_layer(name, srcLayer, srcField)
        cls.set_table_path(layer, tablePath)
        return layer


    @classmethod
    def create_qgis_layer(cls, name, srcLayer, srcField):
        uri = qgs.uriFromLayer(srcLayer)
        uri += "&field=guid:text(64)"
        uri += "&field=date:text(32)"
        uri = uri.replace('guid', srcField)
        return QgsVectorLayer(uri, name, 'memory')


    @classmethod
    def start(cls, tablePath, srcLayer, srcField):
        layer = cls.get_qgis_layer(tablePath, srcLayer, srcField)
        return cls(layer)

    ########################################################################
    ########################################################################
    _TYPES = (
        Qgis.GeometryType.Point,
        Qgis.GeometryType.Line,
        Qgis.GeometryType.Polygon)

    def loadStyle(self):
        # Try tablePath first
        if super().loadStyle(): return True
        # Otherwise use local files
        layer = self._layer
        if layer and layer.isValid():
            type = layer.geometryType()
            type = self._TYPES.index(type)
            name = 'resultlayer_style_{}.qml'.format(type)
            path = _itempath(name)
            return self.applyStyle(path)
        return False




    def _append_feature(self, feat):
        if not feat[1]:
            feat[1] = local_time_as_str()
        self._layer.addFeature(feat)

    def parsedItems(self):
        for guid, feat in self.items():
            if feat.get('label'): yield guid, feat

    def unparsedItems(self):
        for guid, feat in self.items():
            if not feat.get('label'): yield guid, feat

    def hasUnparsedItems(self):
        for guid, feat in self.items():
            if not feat.get('label'): return True
        return False

    def selectUnparsedItems(self):
        fids = [f._fid for _,f in self.unparsedItems()]
        self._layer.selectByIds(fids)




