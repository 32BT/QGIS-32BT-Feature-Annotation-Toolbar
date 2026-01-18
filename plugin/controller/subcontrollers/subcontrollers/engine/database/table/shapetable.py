
import os, json
from ._table import Table
from ._tables import Tables
from qgis.core import QgsGeometry

################################################################################
### ShapeTable
################################################################################

class ShapeTable(Table):
    ITEM_EXT = '.json'

    def saveTableItem(self, guid, shape):
        text = shape.asJson(3)
        if text: super().saveTableItem(guid, text)

    def loadTableItem(self, guid):
        text = super().loadTableItem(guid)
        if text: return QgsGeometry.fromWkt(text)

################################################################################
### UTC relative local time (timezone-aware datetime)
################################################################################

import datetime

def name_from_date(date=None):
    if date is None:
        date = datetime.datetime.now().astimezone()
    if isinstance(date, datetime.datetime):
        date = date.isoformat(timespec='milliseconds')
    name = [c for c in date if c in '0123456789']
    chrs = [c for c in date if c not in '0123456789']
    return ''.join(name)+chrs[-2]

################################################################################
'''
EXPERIMENTAL
ShapesTable is a folder with folders named by guid,
each of which contains json shapefiles named by date.

ShapesTable
    ShapeTable <guid 1>
        <date 1>.json
        <date 2>.json
        ...
    ShapeTable <guid 2>
        <date 1>.json
        <date 2>.json
        ...
    ...

Fetching a ShapesTable item by default fetches the last shape
'''
class ShapesTable(Tables):

    def start(self):
        return super().start(ShapeTable)

    def saveTableItem(self, guid, shape):
        date = name_from_date()
        super().saveTableItem(guid, date, shape)

    def loadTableItem(self, guid, date=None):
        shapeFolder = super().loadTableItem(guid)
        if date is not None:
            name = name_from_date(date)
            return shapeFolder[name]
        else:
            dates = list(sorted(shapeFolder.keys()))
            if dates: return shapeFolder[dates[-1]]

################################################################################
