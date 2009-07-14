import networkx
import numpy

from enthought.enable.api import Container
from enthought.kiva import CAP_BUTT
from enthought.traits.api import Instance, Enum, Bool

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
        
        if not self._graph_layout_needed:
            return
        
        def _apply_graphviz_layout(layout):
            min_x = min([pos[0] for pos in layout.values()])
            max_y = max([pos[1] for pos in layout.values()])
            
            for component in self.components:
                component.x = layout[component._key][0] - min_x
                component.y = self.height - max_y + layout[component._key][1]
        
        if self.style == 'tree':
            layout = tree_layout(self.graph)
            for component in self.components:
                component.x = self.width * layout[component._key][0]
                component.y = self.height * layout[component._key][1]
        elif self.style == 'shell':
            layout = networkx.shell_layout(self.graph)
            for component in self.components:
                component.y = self.width * (1 + layout[component._key][0])/2
                component.x = self.height * (1 + layout[component._key][1])/2
        elif self.style == 'circular':
            layout = networkx.pygraphviz_layout(self.graph, prog='twopi')
            _apply_graphviz_layout(layout)
        else:
            layout = networkx.spring_layout(self.graph)
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
        for edge in self.graph.edges():
            orig = component_dict[edge[0]]
            dest = component_dict[edge[1]]
            
            gc.save_state()
            gc.set_stroke_color((.5,.5,.5))
            
            # TODO: expose weighed parameters
            if self.graph.weighted:
                weight = self.graph[edge[0]][edge[1]]
                if weight < 0.5:
                    phase = 3 * 2.5;
                    pattern = 3 * numpy.array((5,5))
                    gc.set_line_dash(pattern,phase)
                    gc.set_line_cap(CAP_BUTT)
            
            gc.move_to(orig.x + orig.width/2, orig.y)
            gc.line_to(dest.x + dest.width/2, dest.y + dest.height)
            gc.draw_path()
            gc.restore_state()
            
    def _graph_changed(self, new):
        self._graph_layout_needed = True    
