

from .resultfile import ResultFile


################################################################################
### LabelsFile
################################################################################
'''
LabelsFile is a very specific ResultFile. It's a caching CSVFile with
guid,label combos where label is the result.
- It knows about the structure of feat so it can scan specific folders
- It also supports self[guid]=feat so it can be added to an ItemController

Class hierarchy:

    FSItem --> FSFile --> CSVFile --> ResultFile --> LabelsFile

'''

class LabelsFile(ResultFile):

    def scanFeatureFolder(self, folder):
        for guid, feat in folder.items():
            self[guid] = feat['label']

    def scanLabelsFolder(self, folder):
        for labelFolder in folder:
            label = labelFolder.name()
            for guid in labelFolder:
                self[guid] = label

    # So it can be added to an ItemController for guid,feat combos
    def __setitem__(self, guid, item):
        if not isinstance(item, str): item = item['label']
        super().__setitem__(guid, item)
