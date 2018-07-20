from enable.api import BaseTool
from traits.api import HasTraits


class GraphNodeSelectionTool(BaseTool):
    """ Listens for double-clicks and tries to open a traits editor on the
        graph node under the mouse.
    """

    def normal_left_dclick(self, event):
        for node in self.component.components:
            if node.is_in(event.x, event.y):
                if isinstance(node.value, HasTraits):
                    node.value.edit_traits()
                else:
                    node.edit_traits(kind='livemodal')
                break
