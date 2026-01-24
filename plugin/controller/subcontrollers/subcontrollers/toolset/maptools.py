

from qgis.gui import *
from qgis.PyQt.QtCore import *


################################################################################
### Marker MapTool
################################################################################
'''
'''

class MarkerMapTool(QgsMapTool):
    canvasClicked = pyqtSignal(object, object)

    def canvasPressEvent(self, event):
        self._mouseDownPosition = None
        if event.buttons() == Qt.LeftButton:
            self._mouseDownPosition = event.pos()

    def canvasReleaseEvent(self, event):
        if self._mouseDownPosition is not None:
            p = self.snappedPosition(event.pos())
            p = self.toMapCoordinates(p)
            self.canvasClicked.emit(p, event.button())

    def snappedPosition(self, position):
        if self.shouldSnapPosition(position):
            return self._mouseDownPosition
        return position

    def shouldSnapPosition(self, position):
        if hasattr(self, 'tolerance') and self.tolerance:
            dx = abs(position.x()-self._mouseDownPosition.x())
            dy = abs(position.y()-self._mouseDownPosition.y())
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

    def flags(self):
        flags = self.Flag() #super().flags()
        if self._position is None:
            flags |= self.ShowContextMenu
        return flags

    def activate(self):
        super().activate()
        self.resetTracking()

    def resetTracking(self):
        self._tracking = False
        self._position = None

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
