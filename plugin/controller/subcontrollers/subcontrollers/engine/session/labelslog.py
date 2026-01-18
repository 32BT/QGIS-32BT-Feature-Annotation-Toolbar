

from .resultlog import ResultLog


'''
LabelsLog is a very specific ResultLog.
- It knows about the structure of feat so it can read result
- It also supports self[guid]=feat so it can be added to an ItemController

Class hierarchy:

    FSItem --> FSFile --> LOGFile --> ResultLog --> LabelsLog

'''


class LabelsLog(ResultLog):
    def __init__(self, path, name=None):
        super().__init__(path, name)
        if not self.exists():
            self.start('date','user','label','guid')

    def __setitem__(self, guid, feat):
        label = feat['label']
        super().__setitem__(guid, label)
