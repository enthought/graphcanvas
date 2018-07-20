from enable.tools.api import HoverTool
from traits.api import Tuple


class GraphNodeHoverTool(HoverTool):
    _last_xy = Tuple()

    def _is_in(self, x, y):
        return self.component.is_in(x, y)

    def normal_mouse_move(self, event):
        self._last_xy = (event.x, event.y)
        super(GraphNodeHoverTool, self).normal_mouse_move(event)

    def on_hover(self):
        """ This gets called when all the conditions of the hover action have
        been met, and the tool determines that the mouse is, in fact, hovering
        over a target region on the component.

        By default, this method call self.callback (if one is configured).
        """
        for component in self.component.components:
            if component.is_in(*self._last_xy):
                if self.callback is not None:
                    self.callback(component.label)
