import networkx

from enthought.enable.api import Container
from enthought.traits.api import Instance, Enum

class DAGContainer(Container):
    """ Enable Container for Directed Acyclic Graphs
    """
    
    bounds = [350, 350]
    graph = Instance(networkx.DiGraph)
    
    style = Enum('tree', 'shell', 'spring')
    
    def do_layout(self, size=None, force=False):
        """ Nodes of the graph will be layed out based on the the style
            attribute
        """ 
        
        if self.style == 'tree':
            layout = networkx.pygraphviz_layout(self.graph, prog='dot')
            
            min_x = min([pos[0] for pos in layout.values()])
            max_y = max([pos[1] for pos in layout.values()])
            
            for component in self.components:
                component.x = layout[component._key][0] - min_x
                component.y = self.height - max_y + layout[component._key][1]
        elif self.style == 'shell':
            layout = networkx.shell_layout(self.graph)
            for component in self.components:
                component.y = self.width * (1 + layout[component._key][0])/2
                component.x = self.height * (1 + layout[component._key][1])/2
        else:
            layout = networkx.spring_layout(self.graph)
            for component in self.components:
                component.x = self.width * layout[component._key][0]
                component.y = self.height * layout[component._key][1]
            
            

    def draw(self, gc, view_bounds=None, mode="default"):
        if self._layout_needed:
            self.do_layout()

        # draw each component first to ensure their position and size
        # are more or less finalized
        for component in self.components:
            component.draw(gc, view_bounds, mode)

        # draw the connectors
        for component in self.components:
            for child in component.children:
                child_component = None
                for test_component in self.components:
                    if test_component._key == child:
                        child_component = test_component
                        break
                gc.save_state()
                gc.set_stroke_color((.5,.5,.5))
                gc.move_to(component.x + component.width/2, component.y)
                gc.line_to(child_component.x + child_component.width/2, child_component.y + child_component.height)
                gc.draw_path()
                gc.restore_state()
