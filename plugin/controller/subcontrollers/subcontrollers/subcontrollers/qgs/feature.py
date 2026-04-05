

###############################################################################
###
###############################################################################
'''
The problem with QGIS is that they still use QVariant under some circumstances.
A feature attribute which is NULL may return as QVariant(NULL), or as None,
depending on how the value was originally conceived.
QVariant(NULL) == None, evaluates to True
QVariant(NULL) is None, evalautes to False
'''
def getvalue(feature, key):
    try:
        value = feature[key]
        if value != None: return value
    except KeyError: pass

getValue = getvalue

def setvalue(feature, key, value):
    try:
        feature[key] = value
        return True
    except KeyError:
        return False

setValue = setvalue

def getlocation(feature):
    try: return tuple(feature.geometry().centroid().asPoint())
    except Exception: return (0, 0)

getLocation = getlocation

###############################################################################

class Feature:
    def __init__(self, F):
        self._F = F

    def getLocation(self):
        return getLocation(self._F)

    def getValue(self, key):
        return getValue(self._F, key)

    def setValue(self, key, value):
        setValue(self._F, key, value)

