
import os, datetime, json, zlib

from qgis.core import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *

from .. import qgs as QGS
from .marker import Marker

################################################################################
###
################################################################################

def validate_pointgeometry(layer):
    return QGS.LAYER.validate_pointgeometry(layer)


_FIELD_NAMES = ('guid', 'date', 'note')

def validate_fieldnames(layer, requiredFieldNames=_FIELD_NAMES):
    layerFieldNames = layer.fields().names()
    for name in requiredFieldNames:
        if name not in layerFieldNames:
            return False
    return True

################################################################################
_TYPE_KEY = 'tms/layer/type'

class TYPE:
    KEY = _TYPE_KEY
    SOURCE = 'source_layer'
    MAPPED = 'mapped_layer'
    RESULT = 'result_layer'

def set_type(layer, type):
    if layer: layer.setCustomProperty(_TYPE_KEY, type)

def get_type(layer):
    if layer and layer.isValid():
        return layer.customProperty(type)

################################################################################
'''
flag
busy
lock
mask
bits
mark
'''
_URI = '&'.join((
    "Point?crs=epsg:28992",
    "field=flag:text(1)",
    "field=guid:text(32)",
    "field=date:text(32)",
    "field=note:text(190)",
    "index=yes"))

def make(name='Terugmeldingen', crs=None):
    layer = QgsVectorLayer(_URI, name, 'memory')
    set_type(layer, TYPE.SOURCE)
    set_style(layer, 'layer.qml')
    if crs: layer.setCrs(crs)
    return layer


def set_style(layer, fileName=None):
    path = os.path.split(__file__)[0]
    path = os.path.join(path, fileName or 'layer.qml')
    if os.path.exists(path):
        layer.loadNamedStyle(path,
            flags=Qgis.LoadStyleFlag.IgnoreMissingStyleErrors)
    else:
        symbol = layer.renderer().symbol()
        symbol.setColor(QColor.fromRgb(255,255,0))

################################################################################

def validate(layer, mode='r'):
    if is_valid(layer):
        if mode == 'r':
            return True
        if is_writeable(layer):
            return True
    return False


def is_valid(layer):
    if validate_pointgeometry(layer):
        if layer.customProperty(TYPE.KEY):
            return True
        if validate_fieldnames(layer):
            return True
    return False


def is_writeable(layer):
    return layer and layer.isValid() and layer.supportsEditing()

################################################################################

def append_marker(layer, marker):
    F = QgsFeature(layer.fields())
    P = QgsPoint(*marker.location())
    F.setGeometry(P)
    F['guid'] = marker.guid()
    F['date'] = marker.date()
    F['note'] = marker.note()
    appendFeature(layer, F)

def fetch_markers(layer):
    for F in layer.getSelectedFeatures():
        yield Marker.from_qgsfeature(F)

def find_marker(layer, guid):
    for F in layer.getFeatures():
        if F['guid'] == guid:
            return Marker.from_qgsfeature(F)

def update_marker(layer, marker):
    F = next(layer.getSelectedFeatures())
    F['date'] = marker.date()
    F['note'] = marker.note()
    updateFeature(layer, F)

def remove_markers(layer):
    #for F in layer.getSelectedFeatures():
    #    fileAsMarker(layer, F)
    ids = layer.getSelectedFeatureIds()
    QGS.LAYER.deleteFeatures(layer, ids)

################################################################################

def appendFeature(layer, feature):
    QGS.LAYER.appendFeature(layer, feature)
    #saveAsMarker(layer, feature)

def updateFeature(layer, feature):
    QGS.LAYER.updateFeature(layer, feature)
    #saveAsMarker(layer, feature)

def deleteFeature(layer, feature):
    #fileAsMarker(layer, feature)
    QGS.LAYER.deleteFeature(layer, feature.id())


'''
def saveAsMarker(layer, feature):
    session = Session.from_layer(layer)
    if session:
        marker = Marker.from_qgsfeature(feature)
        session.saveMarker(marker)

def fileAsMarker(layer, feature):
    session = Session.from_layer(layer)
    if session:
        marker = Marker.from_qgsfeature(feature)
        session.fileMarker(marker)
'''
################################################################################

