
import os, sys

from qgis.core import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtWidgets import *
from qgis.PyQt.QtGui import *

################################################################################
'''
Default objectname for an action is its name with spaces removed.
This is likely not what we want, as name would be language dependent.
'''
def _objectname(name):
    return "action"+name.replace(" ", "")

################################################################################


class ToolSet(QObject):
    updateAction = pyqtSignal(object, object, object)
    handleAction = pyqtSignal(object, object, object)

    def __init__(self, toolBox, info={}):
        super().__init__()
        self._toolBox = toolBox
        self._actions = []
        self._prepare(toolBox, info)

    def toolBox(self):
        return self._toolBox

    def actions(self):
        return self._actions

    def action(self, idx):
        try: return self._actions[idx]
        except IndexError: pass

    ########################################################################
    ### Prepare
    ########################################################################
    def _prepare(self, toolBox, info={}):
        self._actions = self._prepareActions(info)
        self._prepareToolBox(toolBox, self._actions)

    '''
    Create actions from a dictionary with actionName, iconName pairs.
    '''
    def _prepareActions(self, info={}):
        actions = []
        for name, icon in info.items():
            action = self._prepareAction(icon, name)
            actions.append(action)
        return actions

    def _prepareAction(self, icon, name):
        if isinstance(icon, str):
            icon = self._find_icon(icon)
        action = QAction(icon or QIcon(), name)
        action.setObjectName(_objectname(name))
        action.setEnabled(False)
        return action

    ########################################################################
    '''
    '''
    def _find_icon(self, name):
        name = self._icon_name(name)
        icon = self._load_icon(name)
        if not icon.isNull(): return icon
        if not name.startswith('mAction'):
            return self._find_icon('mAction'+name)
        return QgsApplication.getThemeIcon(name)

    @classmethod
    def _icon_name(cls, name):
        name = name.replace(' ','')
        name, ext = os.path.splitext(name)
        if not ext: ext = '.svg'
        return name+ext

    @classmethod
    def _load_icon(cls, name):
        path = cls._icon_path(name)
        return QIcon(path)

    @classmethod
    def _icon_path(cls, name):
        path = __file__
        path = os.path.split(path)[0]
        path = os.path.join(path, "icons")
        path = os.path.join(path, name)
        return path

    ########################################################################

    def _prepareToolBox(self, toolBox, actions):
        # Add a separator if there are other actions in toolBox
        if toolBox.actions():
            toolBox.addSeparator()
        toolBox.addActions(actions)
        self.getToolBoxTrigger().connect(self.parseToolBoxAction)

    def getToolBoxTrigger(self):
        toolBox = self._toolBox
        try: return toolBox.triggered
        except AttributeError: pass
        try: return toolBox.actionTriggered
        except AttributeError: pass



    def replaceActions(self, info={}):
        beforeAction = self.removeActions()
        self._actions = self._prepareActions(info)
        for action in self._actions:
            self._toolBox.insertAction(beforeAction, action)

    def removeActions(self):
        beforeAction = None
        if self._actions:
            index = self._toolBox.actions().index(self._actions[0])
            for action in self._actions:
                self._toolBox.removeAction(action)
            if index < len(self._toolBox.actions()):
                beforeAction = self._toolBox.actions()[index]
            self._actions = None
        return beforeAction

    ########################################################################
    ### Update
    ########################################################################
    '''
    Controller needs to be able to activate actions in response to signals and
    statechanges.
    '''
    def updateActions(self):
        for idx, action in enumerate(self._actions):
            self.updateAction.emit(self, action, idx)

    def setEnabled(self, enabled=True, index=None):
        if index is None:
            for action in self._actions:
                action.setEnabled(enabled)
        else:
            self._actions[index].setEnabled(enabled)

    def enableActions(self, enable=True):
        for action in self._actions:
            action.setEnabled(enable)

    def enableAction(self, index, enable=True):
        self._actions[index].setEnabled(enable)

    ########################################################################
    ### ToolBar Action Triggered
    ########################################################################
    '''
    ToolSet is a subset of actions in a ToolBar.
    If incoming action belongs to our subset -> parse action.
    '''
    def parseToolBoxAction(self, action):
        if action in self._actions:
            self.parseAction(action)


    '''
    Parse action allows ToolSet to adjust internal state and possibly emit
    a specific signal. Return True to (also) emit the actionTriggered signal
    after parsing action.

    From here:
        ResetTools emits ResetClicked
        IndexTools will update index and buttons, and then emits indexChanged.
        LabelTools extracts labelname from action, and then emits labelClicked
        with that name.
    '''
    def parseAction(self, action):
        idx = self.actions().index(action)
        self.handleAction.emit(self, action, idx)


