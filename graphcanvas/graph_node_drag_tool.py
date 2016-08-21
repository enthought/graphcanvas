from enable.api import BaseTool, Pointer
from traits.api import Either, Float, HasTraits

from graph_node_component import GraphNodeComponent


class GraphNodeDragTool(BaseTool):
    """ Listens for a right click on a graph node and allows the user to
        drag the selected node to a desired location. Edges are redrawn
        live during the node's movement.
    """

    dragging_node = Either(GraphNodeComponent, None)

    normal_pointer = Pointer("arrow")

    moving_pointer = Pointer("hand")

    offset_x = Float

    offset_y = Float

    def dragging_node_default(self):
        return None

    def normal_right_down(self, event):
        for node in self.component.components:
            if node.is_in(event.x, event.y):
                self.dragging_node = node
                self.event_state = "moving"
                event.window.set_pointer(self.moving_pointer)
                event.window.set_mouse_owner(self, event.net_transform())
                self.offset_x = event.x - node.x
                self.offset_y = event.y - node.y
                event.handled = True
        return

    def moving_mouse_move(self, event):
        self.dragging_node.position = [
            event.x - self.offset_x, event.y - self.offset_y
        ]
        event.handled = True
        self.dragging_node.request_redraw()
        return

    def moving_right_up(self, event):
        self.event_state = "normal"
        event.window.set_pointer(self.normal_pointer)
        event.window.set_mouse_owner(None)
        event.handled = True
        self.dragging_node.request_redraw()
        self.dragging_node = None
        return

    def moving_mouse_leave(self, event):
        self.moving_right_up(event)
        event.handled = True
        return
