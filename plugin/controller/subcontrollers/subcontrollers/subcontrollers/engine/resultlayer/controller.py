

from ..database.fsitem import LOGFile

'''
Controller class combines table and layer (model and view)
table = FeatureTable
layer = Layer or derivative
'''

class Controller:
    def __init__(self, table, layer):
        self._table = table
        self._layer = layer

    def __setitem__(self, guid, item):
        self._table[guid] = item
        self._layer[guid] = item

    def __getitem__(self, guid):
        return self._layer[guid]

    def __contains__(self, item):
        if isinstance(item, str):
            return item in self._table

    def mergeSelectedItems(self, srcLayer):
        keys = set(self._table.keys())
        for guid, feat in srcLayer.selectedItems():
            if guid not in keys:
                date = LOGFile.get_date()
                feat.properties = dict(date=date)
                self[guid] = feat
