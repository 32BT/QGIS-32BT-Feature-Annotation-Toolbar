
import os
from .. import FSFolder, FSFile

################################################################################
### Table
################################################################################
'''
A Table is an FSFolder acting as a dictionary for simple textfiles.

    -- table[name] = text --
    will save text to a file named <name>.txt in the folder

    -- text = table[name] --
    will load the contents of <name>.txt as text

    -- del table[name] --
    will delete the file <name>.txt

    -- for name, text in table: --
    iterates all entries in the folder

    -- if name in table: --
    tests whether the file <name>.txt already exists in folder

'''
class Table(FSFolder):
    ITEM_EXT = '.txt'

    @classmethod
    def validateName(cls, name):
        name, ext = os.path.splitext(name)
        if ext == cls.ITEM_EXT: return name

    def keys(self):
        for name in self.itemNames():
            guid = self.validateName(name)
            if guid is not None: yield guid

    def values(self):
        for name in self.itemNames():
            guid = self.validateName(name)
            if guid is not None: yield self[guid]

    def items(self):
        for name in self.itemNames():
            guid = self.validateName(name)
            if guid is not None: yield guid, self[guid]

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
        self.saveItem(name, text)

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

    ########################################################################
    ### CSV
    ########################################################################
    def as_csv(self, hdr=('guid','value')):
        hdr = [','.join(hdr)]
        rws = [','.join(row) for row in self]
        return '\n'.join(hdr+rws)

    def save_as_csv(self, path, hdr=('guid','value')):
        file = FSFile(path)
        file.write(','.join(hdr)+'\n')
        for k, v in self:
            file.write(','.join((k,v))+'\n', 'a')

################################################################################
