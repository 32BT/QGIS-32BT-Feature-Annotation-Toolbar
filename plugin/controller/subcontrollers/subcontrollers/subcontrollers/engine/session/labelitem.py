
'''
A LabelItem acts as glue between internal logic and qgs objects.

The idea is that everything in database is independent from QGIS,
and everything outside uses as little of it as possible.

'''

from qgis.core import *
from qgis.PyQt.QtCore import *

################################################################################
### QGS.FEATURE
################################################################################
'''
QgsFeature annoyingly mixes None and QVariant.NULL
feature.setAttribute(fieldName, None) will set field to NULL, not None
'''
class QGS:
    class FIELDS(QgsFields):
        def append(self, name, size):
            super().append(QgsField(name, QMetaType.QString, len=size))

    class FEATURE:
        def __init__(self, f):
            self._f = f

        def geometry(self):
            return self._f.geometry()

        def properties(self):
            return self._f.attributeMap()

        def __getitem__(self, key):
            return self.get(key)

        def get(self, key):
            try:
                value = self._f[key]
                if value == None: value = None
                return value
            except KeyError:
                if key in ('@shape', 'shape'):
                    return self.geometry()

        def values(self):
            yield self.shape()
            for key in self._f.fields().names():
                yield self[key]

################################################################################

class LabelItem:

    def __init__(self, shape, guid, date, label, comment=None):
        self.shape = shape
        self.guid = guid
        self.date = date
        self.label = label
        self.comment = comment

    ########################################################################
    # This allows item to act as proxy for QgsFeature in FeatureTableFolder
    def geometry(self):
        return self.shape

    def attributes(self):
        return [self.guid, self.date, self.label, self.comment]

    def fields(self, guidFieldName='guid'):
        F = QGS.FIELDS()
        F.append(guidFieldName, 64)
        F.append('date', 32)
        F.append('label', 32)
        if self.comment is not None:
            F.append('comment', 128)
        return F
    ########################################################################
    @classmethod
    def from_qgis_feature(cls, feature):
        F = QGS.FEATURE(feature)
        geom = F.geometry()
        guid = F[0]
        date = F['date']
        label = F['label']
        comment = F['comment']
        return cls(geom, guid, date, label, comment)

    def as_qgis_feature(self, guidFieldName='guid'):
        F = QgsFeature(self.fields(guidFieldName))
        F.setGeometry(self.geometry())
        F[0] = self.guid
        F[1] = self.date
        F[2] = self.label
        if self.comment is not None:
            F[3] = self.comment
        return F
