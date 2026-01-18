'''
EXPERIMENTAL
Tables is a meta Table.
Tables is a TableFolder which has TableFolders as items.
FSFolder.start(<TableFolderClass>) is used to indicate the type of TableFolder.

    TablesFolder(path, name).start(ShapeFolder)

It can be used to implement logging:

    log = TablesFolder(path, name).start(ShapeFolder)
    log[itemName] = itemDate, itemShape

which should create a folder:

    TablesFolder <name>
        ShapeFolder <itemName>
            <itemDate 1>.json
            <itemDate 2>.json
            ...
'''

from ._table import Table

class Tables(Table):
    ITEM_EXT = ''

    def start(self, item_cls):
        self.ITEM_CLS = item_cls
        return super().start()

    def saveTableItem(self, guid, *data):
        name = self.tableItemName(guid)
        item = self.ITEM_CLS(self.path(), name).start()
        if len(data): item.saveTableItem(*data)

    def loadTableItem(self, guid, *keys):
        name = self.tableItemName(guid)
        item = self.ITEM_CLS(self.path(), name).start()
        if len(keys):
            return item.loadTableItem(*keys)
        return item


    # Recursively removing a directory is inherently dangerous
    # TODO: Need some reasonable strategy
    def removeTableItem(self, guid):
        raise NotImplementedError(self.__class__.__name__+'.removeTableItem')
