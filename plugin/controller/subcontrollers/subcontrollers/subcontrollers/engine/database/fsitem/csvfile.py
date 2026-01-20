'''
'''

import os

from .fsfile import FSFile

class CSVFile(FSFile):
    DEFAULT_EXT = '.csv'
    DEFAULT_EOL = '\n'

    @classmethod
    def validateName(cls, name):
        return os.path.splitext(name)[-1].lower() == cls.DEFAULT_EXT

    def __init__(self, path, name=None):
        super().__init__(path, name)
        self._eolc = self.DEFAULT_EOL

    '''
    start is used to start a CSVFile by writing its header.
    It returns self as a convenience.
    '''
    def start(self, *hdr):
        if len(hdr):
            if hdr[0] is None:
                hdr = list(hdr)
                hdr[0] = 'rowid'
        self.writeText(self._merge(hdr))
        return self

    '''
    Fetch columnName at index, or return None
    '''
    def columnName(self, idx):
        if self.exists():
            hdr = self.readHdr()
            if hdr and 0<=idx<len(hdr):
                return hdr[idx]

    ########################################################################
    ### Item Control
    ########################################################################
    '''
    '''
    def __setitem__(self, rowid, data):
        if not isinstance(data, tuple): data = (data,)
        self.appendValues([rowid]+list(data))

    def __getitem__(self, rowid):
        rows = [row for row in self.readRows() if row[0]==rowid]
        if rows:
            row = rows[-1]
            if len(row) == 1: return row[0]
            if len(row) == 2: return row[1]
            return row[1:]

    ########################################################################
    ### Save
    ########################################################################
    
    def appendItems(self, items):
        if not self.exists() and items:
            self.appendValues(items[0].keys())
        for item in items:
            self.appendValues(item.values())

    def appendItem(self, item):
        if not self.exists():
            self.appendValues(item.keys())
        self.appendValues(item.values())

    def appendValues(self, *values):
        txt = self._merge(*values)
        self.writeText(txt, 'a')

    def _merge(self, *values):
        if len(values)==1: values = values[0]
        txt = (str(v).strip() for v in values)
        txt = ','.join(txt) + self._eolc
        return txt

    ########################################################################
    ### Load
    ########################################################################
    def __iter__(self):
        with open(self._path) as f:
            hdr = self._split(next(f))
            for row in f:
                if row.strip():
                    row = self._split(row)
                    yield(dict(zip(hdr, row)))

    def readHdr(self):
        with self.open() as f:
            return self._split(next(f))

    def readRows(self, skip=1):
        with self.open() as f:
            for row in range(skip): next(f)
            for row in f: yield self._split(row)

    def readItems(self):
        return list(iter(self))

    def _split(self, row):
        return [w.strip() for w in row.split(',')]

