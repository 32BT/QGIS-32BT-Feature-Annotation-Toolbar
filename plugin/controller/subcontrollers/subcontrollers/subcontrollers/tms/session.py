

from ..database import FSItem, FSFile, FSFolder, LOGFile
from ..database import JSONTable
from .. import tms as TMS
from .. import qgs as QGS

from .marker import Marker


################################################################################
### Session
################################################################################

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
    _LOG_FILENAME = "log.csv"

    @property
    def logFile(self):
        if not hasattr(self, '_logFile'):
            path = self.itemPath(self._LOG_FILENAME)
            self._logFile = LOGFile(path)
        return self._logFile

    def log(self, actionType, guid, info):
        self.logFile.append(actionType, guid, info)

    ########################################################################
    '''
    A TMS.LAYER will be created with a default style from the plugin folder.
    In order to override the default styling, a qml-file can be saved in
    the session folder.
    '''
    _QML_FILENAME = "lyr.qml"

    @property
    def qmlFile(self):
        return self.itemPath(self._QML_FILENAME)

    ########################################################################
    '''
    CRS authid will be stored in first line of logfile.
    In order to override the CRS, a crs-file can be saved in the sessionfolder.
    '''
    _CRS_FILENAME = "crs.txt"

    @property
    def crsFile(self):
        return self.itemPath(self._CRS_FILENAME)

    ########################################################################
    ########################################################################

    @property
    def crs(self):
        if not hasattr(self, '_crs') or not self._crs:
            crs = FSFile(self.crsFile).readText()
            if crs: crs = crs.strip()
            self._crs = crs or (self.logFile.readHdr() or [None])[-1]
        return self._crs

    @crs.setter
    def crs(self, crs):
        if hasattr(crs, 'authid'): crs = crs.authid()
        self._crs = crs or 'EPSG:4326'

    ########################################################################
    '''
    See FSFolder for logic behind start.

    Use incoming (project) crs for new session.
    Existing sessions will read crs from log file.
    '''
    def start(self, crs):
        if not self.logFile.exists():
            super().start()
            self.crs = crs # <- stuff crs, also translates qgsobject to text
            self.log('CREATE', Marker.class_guid(), self.crs) # <- fetch crs
        return self

    ########################################################################

    # Called from menu interaction
    def start_layer(self, crs):
        self.start(crs)
        layer = TMS.LAYER.make(self.name(), self.crs, self.qmlFile)
        self.set_path(layer, self.path_shrinkuser(self._path))
        self.set_skipcheck(layer, True)
        return QGS.LAYER.add_to_toc(layer)

    # Called from Sentinel
    def refreshLayer(self, layer):
        if self.exists() and self.markersFolder.hasItems():
            for guid, dct in self.markersFolder.items():
                marker = Marker.from_dict(dct)
                if marker: TMS.LAYER.loadMarker(layer, marker)
        return layer

    ########################################################################
    '''
    IMPORTANT: markers are stored as GeoJSON with session.crs coordinates.
    '''

    def saveMarker(self, marker, info=''):
        folder = self.markersFolder.start(Marker)
        exists = folder.saveTableItem(marker.guid(), marker)
        action = ('APPEND', 'MODIFY')[exists]
        self.log(action, marker.guid(), info)

    def fileMarker(self, marker, info=''):
        folder = self.archiveFolder.start()
        format = Marker.JSON.FORMAT.TYPE.COMPACT
        folder.saveItem(marker.guid()+'.json', marker.as_json(format))
        del self.markersFolder[marker.guid()]
        action = ('DELETE', 'ARCHIVE')[bool(info)]
        self.log(action, marker.guid(), info)

