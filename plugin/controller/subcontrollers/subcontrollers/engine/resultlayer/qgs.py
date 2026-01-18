################################################################################

from qgis.core import *
from qgis.PyQt.QtCore import *

_TYPES = (
    Qgis.GeometryType.Point,
    Qgis.GeometryType.Line,
    Qgis.GeometryType.Polygon)


def shapeNameFromType(type):
    if type in _TYPES:
        return type.name
    return 'None'

def shapeNameFromLayer(layer):
    return shapeNameFromType(layer.geometryType())

def crsNameFromLayer(layer):
    return layer.crs().authid()

def uriFromLayer(layer):
    shapeName = shapeNameFromLayer(layer)
    crsName = crsNameFromLayer(layer)
    return "{}?crs={}".format(shapeName, crsName)

