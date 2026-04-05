

import os, datetime, json, zlib

from qgis.core import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *

from .. import qgs as QGS
from .marker import Marker
from .session import Session

from .qml import qml_path

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
    "Point?index=yes",
    # "crs=epsg:28992",
    "field=flag:text(1)",
    "field=guid:text(32)",
    "field=date:text(32)",
    "field=note:text(190)"))

def make(name='Terugmeldingen', crs=None, qml=None):
    layer = QgsVectorLayer(_URI, name, 'memory')
    set_type(layer, TYPE.SOURCE)
    set_crs(layer, crs)
    set_qml(layer, qml)
    return layer


def set_crs(layer, crs):
    if isinstance(crs, str):
        crs = QgsCoordinateReferenceSystem(crs)
    layer.setCrs(crs or QgsProject.instance().crs())

def set_qml(layer, path=''):
    if not (path and os.path.exists(path)):
        path = qml_path()
    set_style(layer, path)

def set_style(layer, path):
    if path and os.path.exists(path):
        layer.loadNamedStyle(path,
        flags=Qgis.LoadStyleFlag.IgnoreMissingStyleErrors)
    else:
        symbol = layer.renderer().symbol()
        symbol.setColor(QColor.fromRgb(255,255,0))

################################################################################

def name_as_json(layer):
    return json.dumps(layer.name())

def crs_as_json(layer):
    return json.dumps(dict(type="name",
    properties=dict(name=layer.crs().toOgcUrn())))

def export_as_json(layer):
    yield '{'
    yield '"type": "FeatureCollection",'
    yield '"name": '+name_as_json(layer)+','
    yield '"crs": '+crs_as_json(layer)+','
    yield '"Features": ['
    n = layer.selectedFeatureCount()
    for F in layer.getSelectedFeatures():
        marker = Marker.from_qgsfeature(F)
        yield json.dumps(marker.as_dict())+('',',')[n>1]
        n -= 1
    yield ']}'

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
    return layer and layer.isValid() and layer.supportsEditing() and not layer.isEditable()

################################################################################

def fetchMarkers(layer):
    for F in layer.getSelectedFeatures():
        yield Marker.from_qgsfeature(F)

def findMarker(layer, guid):
    for F in layer.getFeatures():
        if F['guid'] == guid:
            return Marker.from_qgsfeature(F)

################################################################################
'''
Session.refresh needs to load existing markers into layer,
without rewriting to session.
'''
def loadMarker(layer, marker):
    feature = marker.as_qgsfeature(layer.fields())
    QGS.LAYER.appendFeature(layer, feature)

'''
Append marker to layer and, if available, to session as well.
(Marker is already created, and it is a true append, hence the name.)
'''
def appendMarker(layer, marker):
    feature = marker.as_qgsfeature(layer.fields())
    QGS.LAYER.appendFeature(layer, feature, True)
    session = Session.from_layer(layer)
    if session: session.saveMarker(marker)

def updateMarker(layer, marker):
    F = next(layer.getSelectedFeatures())
    if not QGS.FEATURE.getValue(F, 'guid'):
        QGS.FEATURE.setValue(F, 'guid', marker.guid())
    QGS.FEATURE.setValue(F, 'date', marker.date())
    QGS.FEATURE.setValue(F, 'note', marker.note())
    QGS.LAYER.updateFeature(layer, F)
    session = Session.from_layer(layer)
    if session: session.saveMarker(marker)

'''
In a session, markers are never deleted. Instead, they are always moved to
the archive folder. A removal without reason will be logged by the session
as a delete action.
'''
def removeMarkers(layer, reason=''):
    session = Session.from_layer(layer)
    if session:
        for F in layer.getSelectedFeatures():
            marker = Marker.from_qgsfeature(F)
            session.fileMarker(marker, reason)
    ids = layer.selectedFeatureIds()
    QGS.LAYER.deleteFeatures(layer, ids)

'''
A freeze will be logged as a MODIFY with either the flagvalue or "unflagged".
'''
def freezeMarkers(layer, flag=''):
    if not flag: flag = None
    session = Session.from_layer(layer)
    for F in layer.getSelectedFeatures():
        QGS.FEATURE.setValue(F, 'flag', flag)
        QGS.LAYER.updateFeature(layer, F)
        if session:
            marker = Marker.from_qgsfeature(F)
            info = f"flagged:{flag}" if flag else "unflagged"
            session.saveMarker(marker, info)

################################################################################

def exportMarkers(layer, path, driverName):
    transform_context = QgsProject.instance().transformContext()
    save_options = QgsVectorFileWriter.SaveVectorOptions()
    save_options.driverName = driverName
    save_options.fileEncoding = "UTF-8"
    save_options.onlySelectedFeatures = True
    # WARNING: See also MarkersController.startAppend!!!
    if layer.crs().mapUnits() == QgsUnitTypes.DistanceMeters:
        save_options.layerOptions = ["COORDINATE_PRECISION=3"]
    error = QgsVectorFileWriter.writeAsVectorFormatV3(
        layer, path, transform_context, save_options)
    return error

################################################################################
