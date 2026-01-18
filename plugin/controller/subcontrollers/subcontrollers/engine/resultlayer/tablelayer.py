
import os
from qgis.core import *
from qgis.PyQt.QtCore import *

from .layer import Layer
from ..database import FSItem
from ..database.table import FeatureTable

################################################################################
### Sentinel
################################################################################
'''
In order to prepopulate our TableLayers with features, we use a sentinelobject
to listen for layer-load signals. We only need one global sentinel for the
entire set of plugins.
'''
'''
class Sentinel:
    _key = "tablelayer/sentinel"

    def __init__(self):
        project = QgsProject.instance()
        if not project.property(self._key):
            project.setProperty(self._key, self)
            project.layerWasAdded.connect(self.layerWasAdded)
            for layer in project.mapLayers().values():
                layerWasAdded(layer)

    def layerWasAdded(self, layer):
        if TableLayer.validate(layer):
            if TableLayer.validate_storage(layer):
                if not layer.hasFeatures():
                    TableLayer(layer).refresh()

'''


################################################################################
### TableLayer
################################################################################
'''
TableLayer is a LayerController for layers associated with a featuretable.
A featuretable is merely a folder containing individual GeoJSON features.
'''

class TableLayer(Layer):
    def __init__(self, layer, field=0):
        super().__init__(layer, field)


        self.loadStyle()
        # TODO: move elsewhere
        # Style should only be set once.


    ########################################################################
    ### Table path
    ########################################################################
    '''
    A TableLayer can be considered a view into a FeatureTable.
    The path to the FeatureTable folder is also a unique identifier.
    This allows us to find an existing layer if available.
    '''
    _TABLE_PATH_KEY = "table/path"

    @classmethod
    def validate_layer(cls, layer):
        return bool(layer.customProperty(cls._TABLE_PATH_KEY))

    @classmethod
    def validate_storagetype(cls, layer, storageType='memory'):
        return layer.storageType().lower().startswith(storageType.lower())



    @classmethod
    def validate(cls, layer):
        return bool(layer.customProperty(cls._TABLE_PATH_KEY))

    @classmethod
    def validate_path(cls, layer, path):
        return cls.get_table_path(layer) == path

    @classmethod
    def validate_storage(cls, layer):
        return layer.storageType().lower().startswith('memory')


    @classmethod
    def get_table_path(cls, layer):
        path = layer.customProperty(cls._TABLE_PATH_KEY)
        if path: return FSItem.path_expanduser(path)

    @classmethod
    def set_table_path(cls, layer, path):
        if path: path = FSItem.path_shrinkuser(path)
        if cls.get_table_path(layer) != path:
            layer.setCustomProperty(cls._TABLE_PATH_KEY, path)
            return True
        return False

    @classmethod
    def find_qgis_layer(cls, path):
        for layer in QgsProject.instance().mapLayers().values():
            if path == cls.get_table_path(layer): return layer

    ########################################################################
    '''
    Because we have the table path we can add some additional utilities.
    '''

    def tablePath(self):
        return self.get_table_path(self._layer)

    def tableItemPath(self, name):
        path = self.tablePath()
        if path: return os.path.join(path, name)

    def stylePath(self):
        for name in ('layer', 'style', 'result'):
            path = self.tableItemPath(name+'.qml')
            if os.path.exists(path): return path

    '''
    These are called from init when layer is guaranteed to exist
    '''
    def loadStyle(self):
        path = self.stylePath()
        return self.applyStyle(path)

    def refresh(self):
        path = self.tablePath()
        if path:
            table = FeatureTable(path)
            super().refresh(table.items())

    ########################################################################
    ### Table
    ########################################################################
    '''
    Because we have the table path we can also add tablecontrol.
    However, this is not necessarily the smart choice, and therefore:
        UNDER INVESTIGATION / EXPERIMENTAL

    self.refresh() is implemented with a temporary FeatureTable, which is
    more-or-less the point of the FeatureTable/FSFolder construct.
    Manipulating the **content** of FeatureTable however, makes TableLayer a
    controller of FeatureTable, but TableLayer should be considered more like
    a View into FeatureTable.

    See controller.py
    '''
    '''

    def featureTable(self):
        if not hasattr(self, '_table'):
            self._table = FeatureTable(self.tablePath()).start()
        return self._table

    def __setitem__(self, guid, item):
        if hasattr(self, '_table'):
            self._table[guid] = item
        super().__setitem__(guid, item)

    '''
