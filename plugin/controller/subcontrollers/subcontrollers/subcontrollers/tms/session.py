

from ..database import FSItem, FSFile, FSFolder


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
    _MARKERS_FOLDER_NAME = "markers"
    _ARCHIVE_FOLDER_NAME = "archive"

    def getMarkersFolder(self):
        path = self.itemPath(self._MARKERS_FOLDER_NAME)
        return FSFolder(path).start()

    def getArchiveFolder(self):
        path = self.itemPath(self._ARCHIVE_FOLDER_NAME)
        return FSFolder(path).start()

    def saveMarker(self, marker):
        folder = self.getMarkersFolder()
        folder.saveItem(marker.guid()+'.json', marker.as_json())

    def fileMarker(self, guid):
        pass
