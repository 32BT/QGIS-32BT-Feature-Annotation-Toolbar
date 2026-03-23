

import os, time, datetime

from .fsitem import FSItem
from .fsfile import FSFile

################################################################################
'''
start
-----
If path does not exist, it will be created as folder (recursively if necessary).
If path does exist, it will just return self.
Note however that subclasses may do additional stuff. It is very useful to
supply additional parameters:

    CustomFolder(parent_path, name).start(<parameters>)

The basic idea is that any FSItem type should initially reference its path only
and not create anything until requested to do so, specifically:

    FSFolder(path).exists()

should return False if there is no item at path.
It should not try to create it first.
'''

class FSFolder(FSItem):
    @classmethod
    def validate_path(cls, path):
        return FSItem.path_isdirectory(path)

    def __init__(self, path, name=None):
        super().__init__(path, name)
        if self.isFile():
            raise ValueError('path already exists as file:\n{}'.format(path))

    def start(self):
        if not self.exists():
            os.makedirs(self.path())
        elif self.isFile():
            raise ValueError('path already exists as file:\n{}'.format(path))
        return self

    def isValid(self):
        return self.isDirectory()

    ########################################################################
    ### Content
    ########################################################################
    '''
    Override + namingconvenience for testing subitems easily.
    '''
    def exists(self, itemName=''):
        path = self.itemPath(itemName)
        return os.path.exists(path)

    def itemExists(self, itemName=''):
        return self.exists(itemName)

    def isFile(self, itemName=''):
        path = self.itemPath(itemName)
        return self.path_isfile(path)

    def itemIsFile(self, name=''):
        return self.isFile(name)

    def isFolder(self, itemName=''):
        path = self.itemPath(itemName)
        return self.path_isdirectory(path)

    def itemIsFolder(self, name=''):
        return self.isFolder(name)

    ########################################################################
    '''

    '''
    @classmethod
    def generateItemName(cls):
        date = datetime.datetime.now()
        name = str(date)
        name = ''.join(c for c in name if c in '0123456789')
        name = name[:8]
        return name

    # FSFolder is valid, even with zero itemCount
    def __bool__(self):
        return not self.isFile()

    def __len__(self):
        return self.itemCount()

    def __contains__(self, name):
        return self.itemExists(name)

    def itemPath(self, itemName=''):
        return os.path.join(self.path(), itemName)

    def itemCount(self):
        return len(list(self.itemNames()))

    def hasItems(self):
        for name in self.itemNames():
            return True
        return False

    def itemNames(self, filterProc=None):
        if not self.exists(): return []
        return filter(filterProc, os.listdir(self._path))

    def fileItemNames(self):
        return self.itemNames(self.isFile)

    def folderItemNames(self):
        return self.itemNames(self.isFolder)

    def itemNamesWithExt(self, ext=None):
        return self.itemNames(lambda n: n.endswith(ext))

    ########################################################################
    ### Default to Textfiles
    ########################################################################
    def saveItem(self, name, text):
        path = self.itemPath(name)
        used = os.path.exists(path)
        FSFile(path).writeText(text)
        return used

    def loadItem(self, name):
        path = self.itemPath(name)
        return FSFile(path).readText()

    # TODO: directory removal strategy
    def removeItem(self, itemName):
        itemPath = self.itemPath(itemName)
        if os.path.exists(itemPath):
            os.remove(itemPath)
            return True
        return False

    def trash(self, itemName):
        srcPath = self.itemPath(itemName)
        if os.path.exists(srcPath):
            itemName = str(time.monotonic_ns())+'_'+itemName
            trash = self.__class__(self.itemPath('.trash')).start()
            dstPath = trash.itemPath(itemName)
            os.rename(srcPath, dstPath)
            return True
        return False

################################################################################
