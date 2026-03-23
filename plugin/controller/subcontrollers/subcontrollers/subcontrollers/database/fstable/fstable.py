

import os
from ..fsitem import FSFolder, FSFile

################################################################################
### FSTable
################################################################################
'''
An FSTable is an FSFolder acting as a dictionary for simple textfiles.

    -- table[name] = text --
    will save text to a file named <name>.txt in the folder

    -- text = table[name] --
    will load the contents of <name>.txt as text

    -- del table[name] --
    will delete the file <name>.txt

    -- for name, text in table.items(): --
    iterates all entries in the folder

    -- if name in table: --
    tests whether the file <name>.txt already exists in folder

'''
class FSTable(FSFolder):
    ITEM_EXT = '.txt'

    @classmethod
    def validateName(cls, name):
        name, ext = os.path.splitext(name)
        if ext == cls.ITEM_EXT: return name

    def itemNames(self):
        for name in super().itemNames():
            guid = self.validateName(name)
            if guid is not None: yield guid

    def keys(self):
        return self.itemNames()

    def values(self):
        for guid in self.itemNames():
            yield self[guid]

    def items(self):
        for guid in self.itemNames():
            yield guid, self[guid]

    ########################################################################

    def __iter__(self):
        return self.keys()

    ########################################################################

    def __setitem__(self, guid, text):
        self.saveTableItem(guid, text)

    def __getitem__(self, guid):
        return self.loadTableItem(guid)

    def __delitem__(self, guid):
        self.removeTableItem(guid)

    def __contains__(self, guid):
        return self.tableItemExists(guid)

    ########################################################################

    def saveTableItem(self, guid, text):
        name = self.tableItemName(guid)
        return self.saveItem(name, text)

    def loadTableItem(self, guid):
        name = self.tableItemName(guid)
        return self.loadItem(name)

    def removeTableItem(self, guid):
        name = self.tableItemName(guid)
        return self.removeItem(name)

    def tableItemExists(self, guid):
        name = self.tableItemName(guid)
        return self.exists(name)

    def tableItemName(self, guid):
        return str(guid)+self.ITEM_EXT

################################################################################
