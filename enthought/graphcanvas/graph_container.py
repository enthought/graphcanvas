import networkx
import numpy

from enthought.enable.api import Container
from enthought.kiva.constants import CAP_BUTT
from enthought.traits.api import Instance, Enum, Bool, Property

from layout import tree_layout

class GraphContainer(Container):
    """ Enable Container for Directed Acyclic Graphs
    """

    bounds = [350, 350]
    graph = Instance(networkx.Graph)

    style = Enum('spring', 'tree', 'shell', 'circular')

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

        if self.style == 'tree':
            layout = networkx.pygraphviz_layout(self.graph, prog='dot')

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

            _apply_graphviz_layout(layout)

        elif self.style == 'shell':
            layout = networkx.shell_layout(self.graph)

            # resize the bounds to fit the graph
            radius = numpy.log2(len(layout))
            self.bounds = [max(75, self.components[0].width)*2*radius,
                           max(50, self.components[0].height)*2*radius]

            for component in self.components:
                component.y = self.height * (1 + layout[component._key][0])/2
                component.x = self.width * (1 + layout[component._key][1])/2
        elif self.style == 'circular':
            layout = networkx.pygraphviz_layout(self.graph, prog='twopi')

            # resize the bounds to fit the graph
            radius = numpy.log2(len(layout))
            self.bounds = [max(75, self.components[0].width)*2*radius,
                           max(50, self.components[0].height)*2*radius]

            _apply_graphviz_layout(layout)
        else:
            layout = networkx.spring_layout(self.graph)

            # resize the bounds to fit the graph
            radius = numpy.log2(len(layout))
            self.bounds = [max(75, self.components[0].width)*2*radius,
                           max(50, self.components[0].height)*2*radius]

            for component in self.components:
                component.x = self.width * layout[component._key][0]
                component.y = self.height * layout[component._key][1]

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
        for edge in self.graph.edges():
            orig = component_dict[edge[0]]
            dest = component_dict[edge[1]]

            if orig.y < dest.y:
                # up
                orig_y = orig.y + dest.height/2
                dest_y = dest.y
            else:
                # down
                orig_y = orig.y + dest.height/2
                dest_y = dest.y + dest.height

            if orig.x < dest.x:
                # right
                orig_x = orig.x + orig.width
                dest_x = dest.x + dest.width/2
            else:
                # left
                orig_x = orig.x
                dest_x = dest.x + dest.width/2

            line_starts.append([orig_x, orig_y])
            line_ends.append([dest_x, dest_y])

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

                if self.graph.is_directed():
                    gc.set_fill_color((.5,.5,.5,1))
                    if orig.x < dest.x:
                        gc.arc(orig_x, orig_y, 3, -numpy.pi/2, numpy.pi/2)
                    else:
                        gc.arc(orig_x, orig_y, -3, -numpy.pi/2, numpy.pi/2)

                gc.move_to(orig_x, orig_y)
                gc.line_to(dest_x, dest_y)
                gc.draw_path()

        line_starts = numpy.array(line_starts)
        line_ends = numpy.array(line_ends)


        if self.graph.is_directed():
            a = 0.707106781   # sqrt(2)/2
            vec = line_ends - line_starts
            unit_vec = vec / numpy.sqrt(vec[:,0] ** 2 + vec[:,1] ** 2)[:, numpy.newaxis]

            with gc:
                gc.set_fill_color((1,1,1,0))

                # Draw the left arrowhead (for an arrow pointing straight up)
                arrow_ends = line_ends - numpy.array(unit_vec*numpy.matrix([[a, a], [-a, a]])) * 10
                gc.begin_path()
                gc.line_set(line_ends, arrow_ends)
                gc.stroke_path()

                # Draw the right arrowhead (for an arrow pointing straight up)
                arrow_ends = line_ends - numpy.array(unit_vec*numpy.matrix([[a, -a], [a, a]])) * 10
                gc.begin_path()
                gc.line_set(line_ends, arrow_ends)
                gc.stroke_path()

    def _graph_changed(self, new):
        self._graph_layout_needed = True
