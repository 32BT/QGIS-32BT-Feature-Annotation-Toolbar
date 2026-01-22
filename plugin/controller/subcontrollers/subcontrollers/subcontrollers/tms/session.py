

from ..database import FSItem, FSFile, FSFolder
from ..database import JSONTable
from .marker import Marker

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
        if path and FSItem.path_exists(path): return Session(path)

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

