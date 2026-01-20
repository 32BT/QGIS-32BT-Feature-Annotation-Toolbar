
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *

################################################################################
### Imports
################################################################################

# MenuButton requires access to _load_icon
from .toolset import ToolSet

# MenuButton has SessionMenu attached
from ..sessionmenu import SessionMenu

################################################################################
### MenuButton
################################################################################

class MenuButton:

    def __init__(self, toolBar, iconName="menuButton"):
        '''
        QToolButton with menu does not unraise properly after showing the menu,
        plus the tiny disclosure triangle is not particularely helpful for
        indicating a major InstantPopup.
        So we just build a full actionchain ourselves.
        '''
        self._menu = SessionMenu()
        self._menu.setObjectName("SessionMenu")
        self._menu.aboutToHide.connect(self.menuDidFinish)

        self._action = QAction()
        self._action.setObjectName("SessionMenuAction")
        self._action.setIcon(ToolSet._load_icon(iconName))
        self._action.setText(self._menu.title())
        self._action.triggered.connect(self.showMenu)
        #self._actions.append(self._action)

        self._button = QToolButton()
        self._button.setObjectName("SessionMenuButton")
        self._button.setDefaultAction(self._action)
        toolBar.addWidget(self._button)

    ########################################################################
    '''
    updateAction is triggered by selectionChanged signal via Controller.
    It allows a toolsetcontroller to determine the availability of its buttons.
    This controller manages one button only, the SelectionMenu button.
    '''
    def updateAction(self):
        # Allow delegate to solve the button validation
        self._menu.updateAction.emit(self, self._action, self._menu.BUTTON.INDEX)

    def getMenu(self):
        return self._menu

    def getAction(self):
        return self._action

    def getButton(self):
        return self._button

    ########################################################################

    def showMenu(self, action):
        button = self._button
        button.setDown(True)
        x, y = 0, button.frameSize().height()
        self._menu.popup(button.mapToGlobal(QPoint(x,y)))
        return True

    def menuDidFinish(self):
        self._button.setDown(False)

