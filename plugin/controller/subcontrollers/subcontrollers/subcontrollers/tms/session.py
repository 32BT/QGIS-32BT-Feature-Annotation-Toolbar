

from ..database import FSItem, FSFile, FSFolder
from ..database import JSONTable
from .marker import Marker
from .. import tms as TMS
from .. import qgs as QGS

class Session(FSFolder):

    _SESSIONPATH_KEY = "tms/session/path"

    @classmethod
    def validate_layer(cls, layer):
        return (hasattr(layer, 'customProperty') and
        bool(layer.customProperty(cls._SESSIONPATH_KEY)))

    @classmethod
    def get_path(cls, layer):
        path = layer.customProperty(cls._SESSIONPATH_KEY)
        if path: return FSItem.path_expanduser(path)

    @classmethod
    def set_path(cls, layer, path):
        if path: path = FSItem.path_shrinkuser(path)
        layer.setCustomProperty(cls._SESSIONPATH_KEY, path)

    @classmethod
    def set_skipcheck(cls, layer, skipCheck=True):
        layer.setCustomProperty("skipMemoryLayersCheck", skipCheck)


    @classmethod
    def from_layer(cls, layer):
        path = cls.get_path(layer)
        if path: return Session(path)

    # Called from menu interaction
    def start_layer(self, name=None, crs=None):
        layer = TMS.LAYER.make(name or self.name(), crs)
        self.set_path(layer, self.path_shrinkuser(self._path))
        self.set_skipcheck(layer, True)
        return QGS.LAYER.add_to_toc(layer)

    # Called from Sentinel
    def refreshLayer(self, layer=None):
        if self.exists() and self.markersFolder.hasItems():
            for guid, dct in self.markersFolder.items():
                marker = Marker.from_dict(dct)
                TMS.LAYER.appendMarker(layer, marker)
        return layer

    ########################################################################
    ###
    ########################################################################
    '''
    The two main "tables" in a session "database" are:
        1. Markers; a folder holding active markers as geojson files
        2. Archive; a folder holding archived markers as geojson files
    '''
    _MARKERS_FOLDER_NAME = "markers"
    _ARCHIVE_FOLDER_NAME = "archive"

    @property
    def markersFolder(self):
        if not hasattr(self, '_markersFolder'):
            path = self.itemPath(self._MARKERS_FOLDER_NAME)
            self._markersFolder = JSONTable(path)
        return self._markersFolder

    @property
    def archiveFolder(self):
        if not hasattr(self, '_archiveFolder'):
            path = self.itemPath(self._ARCHIVE_FOLDER_NAME)
            self._archiveFolder = FSFolder(path)
        return self._archiveFolder

    ########################################################################

    def saveMarker(self, marker):
        folder = self.markersFolder.start(Marker)
        folder.saveTableItem(marker.guid(), marker)
        #format = Marker.JSON.FORMAT.TYPE.COMPACT
        #folder.saveItem(marker.guid()+'.json', marker.as_json(format))

    def fileMarker(self, guid):
        srcFolder = self.markersFolder
        dstFolder = self.archiveFolder.start()
        srcPath = srcFolder.itemPath(guid+'.json')
        dstPath = dstFolder.itemPath(guid+'.json')
        FSItem(srcPath).moveTo(dstPath, True)

