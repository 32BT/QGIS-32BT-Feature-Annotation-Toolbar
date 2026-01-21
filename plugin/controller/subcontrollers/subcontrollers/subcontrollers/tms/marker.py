

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
from .. import qgs as QGS

################################################################################
### Marker
################################################################################

class Marker:
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

    @classmethod
    def from_qgsfeature(cls, F):
        P = tuple(F.geometry().asPoint())
        flag = QGS.FEATURE.getValue(F, 'flag')
        guid = QGS.FEATURE.getValue(F, 'guid')
        date = QGS.FEATURE.getValue(F, 'date')
        note = QGS.FEATURE.getValue(F, 'note')
        return Marker(P, note, date, guid)

    @classmethod
    def from_json(cls, src):
        # Allow json-string or json-dict
        if isinstance(src, str): src = json.loads(txt)
        P = src.get('properties') or {}
        flag = P.get('flag')
        guid = P.get('guid')
        date = P.get('date')
        note = P.get('note')
        G = src.get('geometry') or {}
        P = G.get('coordinates') or (0,0)
        return Marker(P, note, date, guid, flag)

    def as_json(self, precision=3):
        P = [_round(p, precision) for p in self._location]
        G = dict(type="Point", coordinates=P)
        P = dict()
        if self._flag: P['flag'] = self._flag
        if self._guid: P['guid'] = self._guid
        if self._date: P['date'] = self._date
        if self._note: P['note'] = self._note
        D = dict(geometry=G, properties=P)
        return json.dumps(D, indent=2)

    ########################################################################
