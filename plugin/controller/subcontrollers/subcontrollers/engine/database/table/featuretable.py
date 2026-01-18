
################################################################################
### FeatureTable
################################################################################

from ._table import Table
from ..feature import Feature

class FeatureTable(Table):
    ITEM_EXT = '.json'

    def saveTableItem(self, guid, feature):
        text = feature.as_json()
        if text: super().saveTableItem(guid, text)

    def loadTableItem(self, guid):
        text = super().loadTableItem(guid)
        if text: return Feature.from_json(text)

    ########################################################################

    def features(self):
        return self.values()

    ########################################################################
