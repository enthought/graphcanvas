from enable.tools.api import ValueDragTool


class GraphNodeDragTool(ValueDragTool):
    """ Listens for a right click on a graph node and allows the user to
        drag the selected node to a desired location. Edges are redrawn
        live during the node's movement.
    """

    drag_button = 'right'

    x_name = 'x'

    y_name = 'y'

    def get_value(self):
        for node in self.component.components:
            if node.is_in(*self.original_screen_point):
                return node

    def set_delta(self, value, delta_x, delta_y):
        if value is not None:
            value.x = self.original_screen_point[0] + delta_x
            value.y = self.original_screen_point[1] + delta_y
            value.request_redraw()

    def dragging(self, event):
        event.window.set_pointer("hand")
        super(GraphNodeDragTool, self).dragging(event)
