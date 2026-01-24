

from qgis.gui import *
from qgis.PyQt.QtCore import *


################################################################################
### Marker MapTool
################################################################################
'''
'''

class MarkerMapTool(QgsMapTool):
    canvasClicked = pyqtSignal(object, object)

    def __init__(self, canvas):
        super().__init__(canvas)
        self._position = None

    def activate(self):
        super().activate()
        self._position = None

    def flags(self):
        flags = super().flags
        if self._position is None:
            flags |= self.ShowContextMenu
        return flags

    def canvasPressEvent(self, event):
        if self._position is None:
            if event.button() == Qt.LeftButton:
                self._position = event.pos()

    def canvasReleaseEvent(self, event):
        if self._position is not None:
            if not event.buttons():
                p = self.snappedPosition(event.pos())
                p = self.toMapCoordinates(p)
                self.canvasClicked.emit(p, event.button())
                self._position = None

    def snappedPosition(self, position):
        if self.shouldSnapPosition(position):
            return self._mouseDownPosition
        return position

    def shouldSnapPosition(self, position):
        if hasattr(self, 'tolerance') and self.tolerance:
            dx = abs(position.x()-self._position.x())
            dy = abs(position.y()-self._position.y())
            return (dx*dx+dy*dy)<=(self.tolerance*self.tolerance)

################################################################################
### Marker MapTool with panning
################################################################################

class PanningMarkerMapTool(QgsMapTool):
    canvasClicked = pyqtSignal(object, object)

    def __init__(self, canvas):
        super().__init__(canvas)
        self.resetTracking()
        self.tolerance = 5

    def activate(self):
        super().activate()
        self.resetTracking()

    def resetTracking(self):
        self._tracking = False
        self._position = None

    def flags(self):
        flags = super().flags()
        if self._position is None:
            flags |= self.ShowContextMenu
        return flags

    '''
    If right-button is pressed before left-button, then contextmenu takes over.
    Otherwise, the left-button starts a click or pan action.
    If right-button is pressed after left-button, then we should continue our
    current action. Panning gets confused by additional button presses, likely
    because of lastMouseXY, we therefore reset panAction.
    '''
    def canvasPressEvent(self, event):
        if self._tracking:
            self.canvas().panActionEnd(event.pos())
        elif event.buttons() == Qt.LeftButton:
            self._position = event.pos()

    '''
    Convert to pan-action if dragging
    '''
    def canvasMoveEvent(self, event):
        if self._tracking:
            self.canvas().panAction(event)
        elif event.buttons():
            dx = abs(self._position.x()-event.pos().x())
            dy = abs(self._position.y()-event.pos().y())
            self._tracking = (dx*dx+dy*dy)>(self.tolerance*self.tolerance)

    '''
    Stop action when all buttons are released.
    '''
    def canvasReleaseEvent(self, event):
        if not event.buttons():
            if self._tracking:
                self.canvas().panActionEnd(event.pos())
            else:
                mapLocation = self.toMapCoordinates(self._position)
                self.canvasClicked.emit(mapLocation, event.button())
            self.resetTracking()
