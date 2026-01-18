
from ..database import FSFolder, FSFile, FSItem, CSVFile
from .labelfolder import LabelFolder
from .labelsfile import LabelsFile

################################################################################
### LabelsFolder
################################################################################
'''
LabelsFolder is a Folder containing a set of FeatureFolders.
Each FeatureFolder represents a label.
A LabelsFolder may also contain optional metafiles.

LabelsFolder
    labels.csv (index of guid, label combo's equivalent to lyr.csv)
    labels.txt (optional, order of labels in toolbar)
    labels.qml (optional, layerstyling)

    LabelFolder(FeatureFolder) <"Accept">
        icon.svg
        <guid 1>.json
        <guid 2>.json
        ...
    LabelFolder(FeatureFolder) <"Reject">
        icon.svg
        <guid 1>.json
        <guid 2>.json
        ...

Note that LabelsFolder is asymmetric:
It fetches tablefolders, but it stuffs a (guid,feature) combo

    To traverse existing labelfolders, use:
        for labelFolder in self:

    To fetch a labelfolder (creating it if necessary), use:
        labelFolder = self[labelName]

    To stuff a Feature in a labelfolder, use:
        self[labelName] = guid, feature
'''

class LabelsFolder(FSFolder):

    def start(self, row_id='guid'):
        super().start()
        #self.labelsFile(row_id)
        return self

    ########################################################################
    ########################################################################
    '''
    Note: LabelsFolder iterates values, not keys. In this context it makes
    more sense to think of folders in a folder, not itemnames in a folder.
    '''
    def __iter__(self):
        return self.values()

    def keys(self):
        return self.folderItemNames()

    def values(self):
        for label in self.folderItemNames():
            yield self[label]

    def items(self):
        return zip(self.keys(), self.values())

    ########################################################################
    '''
    Setting an item means:
        storing a feature in the labelfolder corresponding to label
    '''
    def __setitem__(self, label, item):
        guid = item[0]
        feat = item[1]
        #self.labelsFile()[guid] = feat

        # Stuff feature in labelfolder
        self[label].saveTableItem(guid, feat)
        # Remove feature from other labelfolders if present
        for labelFolder in self:
            if labelFolder.name() != label:
                labelFolder.removeTableItem(guid)

    '''
    Every path that is not already a file, is valid as a labelfolder path.
    '''
    def __getitem__(self, label):
        path = self.itemPath(label)
        if not FSItem.path_isfile(path):
            return LabelFolder(path).start()
        error = "'{}' already exists as file in labelsfolder '{}'!"
        error = error.format(label, self.name())
        raise KeyError(error)

    ########################################################################
    ### LabelsFile
    ########################################################################
    '''
    labels.csv
    ----------
    Index file with guid/label combos, useable as layer source.
    '''
    def labelsFile(self, row_id='guid'):
        if not hasattr(self, '_labelsFile'):
            path = self.itemPath('labels.csv')
            file = LabelsFile(path).start(row_id, 'label')
            file.scanLabelsFolder(self)
            self._labelsFile = file
        return self._labelsFile

    ########################################################################
    ### Metadata files
    ########################################################################
    '''
    The Labelfolders in self may contain an optional icon.svg file.
    If the icon file is available, its path is returned in labelInfo.
    If the icon file is not available, the labelName will be returned instead.
    In that case the plugin will search for a default icon for that labelName.
    If no (default) icon is found, the labelName itself is used in the toolbar.
    '''
    def labelInfo(self):
        info = {}
        for label in self.labelNames():
            icon = label
            path = self[label].iconPath()
            if FSFile.path_exists(path):
                icon = path
            info[label] = icon
        return info

    '''
    If a labels.txt file exists in self, then the toolbar will create buttons
    in that particular order.
    '''
    def labelNames(self):
        path = self.itemPath('labels.txt')
        if FSFile.validate_path(path):
            rows = list(FSFile(path))
            return filter(None, (row.strip() for row in rows))
        return []

    '''
    If a labels.qml file exists in self, then resultLayer will load this style.
    '''
    def labelStyle(self):
        path = self.itemPath('labels.qml')
        if FSFile.validate_path(path):
            return path
    ########################################################################
