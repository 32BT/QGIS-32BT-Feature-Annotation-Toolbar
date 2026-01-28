

from .action import ActionLink

################################################################################
### ActionSet
################################################################################
'''
ActionSet is a controller for a single set of actions.

e.g.:
    ActionManager(ActionLink)
        TokenTools(ActionSet) <- append, modify, remove
        AdminTools(ActionSet) <- freeze, export, archive

It has convenience functions to add or remove actions in a view.

TODO: the default actionresponder is "self". This may not necessarily be
the desired behavior.
'''
class ActionSet(ActionLink):
    def __init__(self, *actions):
        super().__init__()
        self._actions = actions
        for action in actions:
            action.setResponder(self)

    def getAction(self, idx):
        return self._actions[idx]

    def updateActions(self):
        for action in self._actions: action.update()

    ########################################################################

    def appendTo(self, toolBox):
        if toolBox.actions(): toolBox.addSeparator()
        toolBox.addActions(self._actions)

    def removeFrom(self, toolBox):
        for action in self._actions:
            toolBox.removeAction(action)
        if toolBox.actions(): toolBox.removeAction(toolBox.actions()[-1])


