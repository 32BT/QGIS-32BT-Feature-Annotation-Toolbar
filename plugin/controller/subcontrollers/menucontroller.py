

from .subcontrollers.toolset.menubutton import MenuButton


################################################################################
### MenuController
################################################################################
'''
'''
class MenuController:
    def __init__(self, iface, toolBar):
        self._menuButton = MenuButton(toolBar)

    def updateActions(self):
        self._menuButton.updateAction()

    '''
    Delegate is attached directly to menu.
    Updates channeled by the menu include the menu-toolbarbutton itself,
    see MenuButton.updateAction which uses the menu to emit the updaterequest.
    '''
    def setDelegate(self, delegate):
        menu = self._menuButton.getMenu()
        if hasattr(delegate, "updateMenuAction"):
            menu.updateAction.connect(delegate.updateMenuAction)
        if hasattr(delegate, "handleMenuAction"):
            menu.handleAction.connect(delegate.handleMenuAction)

