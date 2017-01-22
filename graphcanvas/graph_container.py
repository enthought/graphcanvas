import networkx
import numpy

from enable.api import Container
from kiva.constants import CAP_BUTT
from traits.api import Instance, Enum, Bool, Property

from graphcanvas.layout import circular_layout, tree_layout

SUPPORTED_LAYOUTS = ['spring', 'tree', 'shell', 'circular', 'spectral']


class GraphContainer(Container):
    """ Enable Container for Directed Acyclic Graphs
    """

    bounds = [350, 350]
    graph = Instance(networkx.Graph)

    style = Enum(SUPPORTED_LAYOUTS)

    # graph layout is different than Enable's layout: graph layout is
    # the relative positioning on nodes, and is very expensive
    _graph_layout_needed = Bool(True)

    def do_layout(self, size=None, force=False):
        """ Nodes of the graph will be layed out based on the the style
            attribute
        """

        if not self._graph_layout_needed or len(self.components) == 0:
            return

        def _apply_graphviz_layout(layout):
            min_x = min([pos[0] for pos in layout.values()])
            max_y = max([pos[1] for pos in layout.values()])

            for component in self.components:
                component.x = layout[component._key][0] - min_x
                component.y = self.height - max_y + layout[component._key][1]

        initial_positions = {
            node.value: node.position for node in self.components
        }
        if all(point == [0.0, 0.0] for point in initial_positions.values()):
            initial_positions = None

        scale = min(self.bounds)

        if self.style == 'tree':
            try:
                layout = networkx.drawing.nx_agraph.pygraphviz_layout(
                    self.graph, prog='dot'
                )
                _apply_graphviz_layout(layout)
            except ImportError:
                layout = tree_layout(self.graph)

                # resize the bounds to fit the graph
                depths = [v[1] for v in layout.values()]
                widths = [depths.count(d) for d in numpy.unique(depths)]
                max_width = max(widths)
                max_depth = len(widths)

                self.bounds = [max(75, self.components[0].width)*max_width,
                               max(50, self.components[0].height)*max_depth]

                for component in self.components:
                    component.x = self.width * layout[component._key][0]
                    component.y = self.height * layout[component._key][1]

        elif self.style == 'shell':
            layout = networkx.shell_layout(self.graph)

            # resize the bounds to fit the graph
            radius = numpy.log2(len(layout))
            self.bounds = [max(75, self.components[0].width)*2*radius,
                           max(50, self.components[0].height)*2*radius]

            for component in self.components:
                component.y = self.height * (1 + layout[component._key][0])/2
                component.x = self.width * (1 + layout[component._key][1])/2

        elif self.style == 'spectral':
            layout = networkx.spectral_layout(self.graph)

            # resize the bounds to fit the graph
            radius = numpy.log2(len(layout))
            self.bounds = [max(75, self.components[0].width)*2*radius,
                           max(50, self.components[0].height)*2*radius]

            for component in self.components:
                component.y = self.height * (1 + layout[component._key][0])/2
                component.x = self.width * (1 + layout[component._key][1])/2

        elif self.style == 'circular':
            try:
                layout = networkx.drawing.nx_agraph.pygraphviz_layout(
                    self.graph, prog='twopi'
                )
            except ImportError:
                layout = circular_layout(self.graph)

            # resize the bounds to fit the graph
            radius = numpy.log2(len(layout))
            self.bounds = [max(75, self.components[0].width)*2*radius,
                           max(50, self.components[0].height)*2*radius]

            _apply_graphviz_layout(layout)
        else:
            layout = networkx.spring_layout(
                self.graph,
                pos=initial_positions,
                scale=scale,
            )

            # resize the bounds to fit the graph
            radius = len(layout)
            self.bounds = [max(75, self.components[0].width)*2*radius,
                           max(50, self.components[0].height)*2*radius]

            for component in self.components:
                component.x = layout[component._key][0]
                component.y = layout[component._key][1]

        self._graph_layout_needed = False


    def draw(self, gc, view_bounds=None, mode="default"):
        if self._layout_needed:
            self.do_layout()

        # draw each component first to ensure their position and size
        # are more or less finalized
        component_dict = {}
        for component in self.components:
            component.draw(gc, view_bounds, mode)
            component_dict[component.value] = component

        # draw the connectors
        # connectors will always originate on a side
        # and terminate on the top or bottom

        line_starts = []
        line_ends = []
        line_ctrl1s = []
        line_ctrl2s = []
        for edge in self.graph.edges():
            orig = component_dict[edge[0]]
            dest = component_dict[edge[1]]

            dx = orig.x - dest.x
            dy = orig.y - dest.y

            orig_x = orig.x + orig.width/2.
            orig_y = orig.y + orig.height/2.
            ctrl1_x = orig_x
            ctrl1_y = orig_y
            dest_x = dest.x + dest.width/2.
            dest_y = dest.y + dest.height/2.
            ctrl2_x = dest_x
            ctrl2_y = dest_y

            if dy > abs(dx):
                # origin is above destination, so connect bottom to top
                orig_y = orig.y
                ctrl1_y = orig.y - dy/3.0
                ctrl2_y = dest.y + dest.height + dy/3.0
                dest_y = dest.y + dest.height
            elif dy < -abs(dx):
                # origin is below destination, so connect top to bottom
                orig_y = orig.y + orig.height
                ctrl1_y = orig.y + orig.height - dy/3.0
                ctrl2_y = dest.y + dy/3.0
                dest_y = dest.y
            elif dx > abs(dy):
                # origin is right of destination, so connect left to right
                orig_x = orig.x
                ctrl1_x = orig.x - dx/3.0
                ctrl2_x = dest.x + dest.width + dx/3.0
                dest_x = dest.x + dest.width
            elif dx < -abs(dy):
                # origin is left of destination, so connect right to left
                orig_x = orig.x + orig.width
                ctrl1_x = orig.x + orig.width - dx/3.0
                ctrl2_x = dest.x + dx/3.0
                dest_x = dest.x
            else:
                # edge is self-loop, connect left to bottom
                orig_x = orig.x + orig.width
                ctrl1_x = orig.x + 3*orig.width
                ctrl2_y = dest.y - 2*dest.height
                dest_y = dest.y


            line_starts.append([orig_x, orig_y])
            line_ends.append([dest_x, dest_y])
            line_ctrl1s.append([ctrl1_x, ctrl1_y])
            line_ctrl2s.append([ctrl2_x, ctrl2_y])

            with gc:
                gc.set_stroke_color((.5,.5,.5))
                gc.set_fill_color((1,1,1,0))

                # TODO: expose weighed parameters
                attributes = self.graph.get_edge_data(*edge)
                if 'weight' in attributes:
                    weight = attributes['weight']
                    if weight < 0.5:
                        phase = 3 * 2.5;
                        pattern = 3 * numpy.array((5,5))
                        gc.set_line_dash(pattern,phase)
                        gc.set_line_cap(CAP_BUTT)

                gc.move_to(orig_x, orig_y)
                gc.curve_to(ctrl1_x, ctrl1_y, ctrl2_x, ctrl2_y, dest_x, dest_y)
                gc.draw_path()

        line_starts = numpy.array(line_starts)
        line_ends = numpy.array(line_ends)
        line_ctrl1s = numpy.array(line_ctrl1s)
        line_ctrl2s = numpy.array(line_ctrl2s)

        if self.graph.is_directed():
            with gc:
                gc.set_fill_color((.5,.5,.5,1))
                for (x, y), (dx, dy) in zip(line_starts, line_ctrl1s-line_starts):
                    gc.move_to(x, y)
                    if dx < 0:
                        gc.arc(x, y, 3, numpy.pi/2, 3*numpy.pi/2)
                    elif dy > 0:
                        gc.arc(x, y, 3, 0, numpy.pi)
                    elif dx > 0:
                        gc.arc(x, y, 3, numpy.pi/2, -numpy.pi/2)
                    else:
                        gc.arc(x, y, 3, -numpy.pi, 0)
                gc.draw_path()

            s = 0.5
            c = 0.8660254037844386  # cos(pi/6.0)0.707106781   # sqrt(2)/2
            vec = line_ends - line_ctrl2s
            if len(vec) == 0:
                return
            unit_vec = vec / numpy.sqrt(vec[:,0] ** 2 + vec[:,1] ** 2)[:, numpy.newaxis]

            with gc:
                gc.set_fill_color((1,1,1,0))

                # Draw the left arrowhead (for an arrow pointing straight up)
                arrow_ends = line_ends - numpy.array(unit_vec*numpy.matrix([[c, s], [-s, c]])) * 10
                gc.begin_path()
                gc.line_set(line_ends, arrow_ends)
                gc.stroke_path()

                # Draw the right arrowhead (for an arrow pointing straight up)
                arrow_ends = line_ends - numpy.array(unit_vec*numpy.matrix([[c, -s], [s, c]])) * 10
                gc.begin_path()
                gc.line_set(line_ends, arrow_ends)
                gc.stroke_path()

    def _graph_changed(self, new):
        self._graph_layout_needed = True
