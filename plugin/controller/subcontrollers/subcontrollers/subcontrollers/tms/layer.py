
import os, datetime, json, zlib

from qgis.core import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *

from .. import qgs as QGS
from .marker import Marker
from .session import Session

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

def fetchMarkers(layer):
    for F in layer.getSelectedFeatures():
        yield Marker.from_qgsfeature(F)

def findMarker(layer, guid):
    for F in layer.getFeatures():
        if F['guid'] == guid:
            return Marker.from_qgsfeature(F)

################################################################################

def appendMarker(layer, marker):
    feature = marker.as_qgsfeature(layer.fields())
    QGS.LAYER.appendFeature(layer, feature)
    session = Session.from_layer(layer)
    if session: session.saveMarker(marker)

def updateMarker(layer, marker):
    F = next(layer.getSelectedFeatures())
    QGS.FEATURE.setValue(F, 'date', marker.date())
    QGS.FEATURE.setValue(F, 'note', marker.note())
    QGS.LAYER.updateFeature(layer, F)
    session = Session.from_layer(layer)
    if session: session.saveMarker(marker)

def removeMarkers(layer):
    session = Session.from_layer(layer)
    if session:
        for F in layer.getSelectedFeatures():
            guid = QGS.FEATURE.getValue(F, 'guid')
            session.fileMarker(guid)
    ids = layer.selectedFeatureIds()
    QGS.LAYER.deleteFeatures(layer, ids)

################################################################################
