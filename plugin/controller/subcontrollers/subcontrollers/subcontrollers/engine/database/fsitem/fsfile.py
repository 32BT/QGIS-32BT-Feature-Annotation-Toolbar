
from .fsitem import FSItem

################################################################################

class FSFile(FSItem):
    @classmethod
    def validate_path(cls, path):
        return FSItem.path_isfile(path)


    def open(self, mode='r', encoding='utf-8'):
        return open(self.path(), mode, encoding=encoding)

    ########################################################################

    def writeText(self, txt, mode='w'):
        with self.open(mode) as f:
            f.write(txt)

    def appendText(self, txt):
        self.writeText(txt, 'a')

    def appendLine(self, txt):
        self.writeText(txt+'\n', 'a')

    ########################################################################

    def readText(self, mode='r'):
        if self.exists():
            with self.open() as f:
                return f.read()

    def readline(self, idx=0):
        with self.open() as f:
            for _ in range(idx): next(f)
            return next(f).strip()

    def __iter__(self):
        with self.open() as f:
            return iter(list(f))

################################################################################
