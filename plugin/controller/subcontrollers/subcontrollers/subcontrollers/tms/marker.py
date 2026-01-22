

################################################################################

import uuid

def local_uuid_as_str():
    return str(uuid.uuid4()).replace('-','')

################################################################################
### UTC relative local time (timezone-aware datetime)
################################################################################

import datetime

def local_time():
    return datetime.datetime.now().astimezone()
def local_time_as_str():
    return local_time().isoformat(timespec='milliseconds')

################################################################################
### Compare round(8.5)
################################################################################

def _round(v, p=3):
    m = 10**p
    i = int(2*m*v)+1-((v<0)<<1)
    return (i//2)/m

################################################################################

import json
from qgis.core import QgsFeature, QgsPoint
from .. import qgs as QGS

################################################################################
### Marker
################################################################################

class Marker:
    @staticmethod
    def class_round(v, p=3):
        if isinstance(v, float): return _round(v, p)
        return v.__class__(*[_round(x, p) for x in v])
    @classmethod
    def class_guid(cls): return local_uuid_as_str()
    @classmethod
    def class_date(cls): return local_time_as_str()

    def __init__(self, location, note, date=None, guid=None, flag=None):
        self._location = location
        self._flag = flag
        self._guid = guid or local_uuid_as_str()
        self._date = date or local_time_as_str()
        self._note = note.strip()

    def location(self):
        return self._location
    def flag(self):
        return self._flag
    def guid(self):
        return self._guid
    def date(self):
        return self._date
    def note(self):
        return self._note

    def replaceNote(self, note):
        note = note.strip()
        if self._note != note:
            self._note = note
            self._date = local_time_as_str()
            return True
        return False

    ########################################################################
    ### QGIS
    ########################################################################

    @classmethod
    def from_qgsfeature(cls, F):
        P = tuple(F.geometry().asPoint())
        flag = QGS.FEATURE.getValue(F, 'flag')
        guid = QGS.FEATURE.getValue(F, 'guid')
        date = QGS.FEATURE.getValue(F, 'date')
        note = QGS.FEATURE.getValue(F, 'note')
        return Marker(P, note, date, guid)

    def as_qgsfeature(self, fields):
        F = QgsFeature(fields)
        P = QgsPoint(*self.location())
        F.setGeometry(P)
        QGS.FEATURE.setValue(F, 'flag', self._flag)
        QGS.FEATURE.setValue(F, 'guid', self._guid)
        QGS.FEATURE.setValue(F, 'date', self._date)
        QGS.FEATURE.setValue(F, 'note', self._note)
        return F

    ########################################################################
    ### JSON
    ########################################################################

    class JSON:
        class FORMAT:
            class TYPE:
                COMPACT = "compact"
                GEOJSON = "geojson"
        class DEFAULT:
            FORMAT = "geojson"
            INDENT = 2

    ########################################################################

    @classmethod
    def from_json(cls, src):
        if isinstance(src, str): src = json.loads(src)
        return cls.from_dict(src)

    def as_json(self, format="geojson"):
        format = (format or self.JSON.DEFAULT.FORMAT).lower()
        if format == self.JSON.FORMAT.TYPE.COMPACT:
            return json.dumps(self.as_properties())
        else:
            return json.dumps(self.as_dict(), indent=self.JSON.DEFAULT.INDENT)

    ########################################################################

    # Also reads compactform
    @classmethod
    def from_dict(cls, src):
        P = src.get('properties') or src
        flag = P.get('flag')
        guid = P.get('guid')
        date = P.get('date')
        note = P.get('note')
        G = src.get('geometry') or {}
        P = G.get('coordinates') or P.get('geom') or (0,0)
        return Marker(P, note, date, guid, flag)

    def as_dict(self):
        P = list(self._location)
        G = dict(type="Point", coordinates=P)
        P = dict()
        if self._flag: P['flag'] = self._flag
        if self._guid: P['guid'] = self._guid
        if self._date: P['date'] = self._date
        if self._note: P['note'] = self._note
        return dict(type="Feature", geometry=G, properties=P)

    ########################################################################
    # Compact form

    def from_properties(cls, P):
        geom = P.get('geom') or (0, 0)
        flag = P.get('flag')
        guid = P.get('guid')
        date = P.get('date')
        note = P.get('note')
        return Marker(geom, note, date, guid, flag)

    def as_properties(self):
        P = list(self._location)
        P = dict(geom=P)
        if self._flag: P['flag'] = self._flag
        if self._guid: P['guid'] = self._guid
        if self._date: P['date'] = self._date
        if self._note: P['note'] = self._note
        return P

    ########################################################################

