################################################################################

import os

def _getcwd():
    return os.path.split(__file__)[0]
################################################################################

import json
from ..database import *
from .resultlog import ResultLog
from .resultfile import ResultFile
from .resulttable import ResultTable
from .labelsfolder import LabelsFolder




###############################################################################
### LabelSession
###############################################################################
'''
SessionFolder is the folder with results.

It contains:
    lyr.csv - simple text table with (guid,label) entries
    log.csv - simple text table with (date,user,label,guid) entries
    Labels - LabelsFolder with GeoJSON features sorted by label
    Features - FeatureFolder with GeoJSON features

The name of the first column in lyr.csv is the name of the joinField.

Note: SessionFolder is QGIS independent.
It is meant to control our internal app-independent database results.
'''
class SessionFolder(FSFolder):

    def __init__(self, path, name=None, field=None):
        super().__init__(path, name)
        self._lyrFile = None
        self._logFile = None
        self._shapesFolder = None
        self._labelsFolder = None

        self._field = field

    ########################################################################
    '''
    During session-dialog we want to fetch joinfield if available
    (without creating any content otherwise).
    '''
    def joinFieldName(self):
        if self._field is None:
            path = self.lyrFilePath()
            self._field = CSVFile(path).columnName(0)
        return self._field

    def setJoinFieldName(self, fieldName):
        self._field = fieldName

    ########################################################################

    def lyrFilePath(self, name="lyr.csv"):
        return self.itemPath(name)

    def logFilePath(self, name="log.csv"):
        return self.itemPath(name)

    def labelsFolderPath(self, name="Labels"):
        return self.itemPath(name)

    def featureTablePath(self, name="Features"):
        return self.itemPath(name)

    ########################################################################

    def _start_lyr_file(self):
        file = ResultFile(self.lyrFilePath())
        if not file.exists():
            file.start(self.joinFieldName(), "label")
        return file

    def _start_log_file(self):
        file = ResultLog(self.logFilePath())
        if not file.exists():
            file.start("date","user","label","guid")
        return file

    def _start_shapes_folder(self):
        return ResultTable(self.featureTablePath()).start()

    def _start_labels_folder(self):
        return LabelsFolder(self.labelsFolderPath()).start(self.joinFieldName())

    ########################################################################

    @property
    def lyrFile(self):
        if self._lyrFile is None:
            self._lyrFile = self._start_lyr_file()
        return self._lyrFile

    @property
    def logFile(self):
        if self._logFile is None:
            self._logFile = self._start_log_file()
        return self._logFile

    @property
    def featureTable(self):
        if self._shapesFolder is None:
            self._shapesFolder = self._start_shapes_folder()
        return self._shapesFolder

    @property
    def labelsFolder(self):
        if self._labelsFolder is None:
            self._labelsFolder = self._start_labels_folder()
        return self._labelsFolder

    ########################################################################

    def labelInfo(self):
        return self.labelsFolder.labelInfo()

    def stylePath(self):
        return self.labelsFolder.labelStyle()

    ########################################################################

    def __getitem__(self, guid):
        return self.featureTable[guid]

    def __setitem__(self, guid, item):
        # Update featuretable
        self.featureTable[guid] = item
        # Update results
        label = item['label']
        self.logFile[guid] = label
        self.lyrFile[guid] = label
        self.labelsFolder[label] = guid, item


