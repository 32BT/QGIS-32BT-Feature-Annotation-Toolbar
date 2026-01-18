

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


class Marker:
    def __init__(self, mapPoint, note, date=None, guid=None):
        self._location = mapPoint
        self._guid = guid or local_uuid_as_str()
        self._date = date or local_time_as_str()
        self._note = note

    def location(self):
        return self._location
    def guid(self):
        return self._guid
    def date(self):
        return self._date
    def note(self):
        return self._note
