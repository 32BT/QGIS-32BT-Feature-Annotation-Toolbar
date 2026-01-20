

from qgis.core import *


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
'''
TODO: move to feature.py as in: QGS.FEATURE.getvalue(F, key)
'''
def _qgsfeature_getvalue(F, key):
    try: return F[key]
    except KeyError: pass


from .. import qgs as QGS

################################################################################

class Marker:
    @classmethod
    def class_guid(cls): return local_uuid_as_str()
    @classmethod
    def class_date(cls): return local_time_as_str()

    @classmethod
    def from_qgsfeature(cls, F):
        P = F.geometry().asPoint()
        flag = QGS.FEATURE.getValue(F, 'flag')
        guid = QGS.FEATURE.getValue(F, 'guid')
        date = QGS.FEATURE.getValue(F, 'date')
        note = QGS.FEATURE.getValue(F, 'note')
        return Marker(P, note, date, guid)


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
