import networkx

from enthought.enable.api import ComponentEditor, Scrolled,Viewport
from enthought.enable.tools.api import ViewportPanTool
from enthought.traits.api import HasTraits, Instance, Dict, Any, Enum
from enthought.traits.ui.api import View, Item

from dag_container import DAGContainer
from graph_container import GraphContainer
from graph_node_component import GraphNodeComponent
from graph_node_selection_tool import GraphNodeSelectionTool
from graph_node_hover_tool import GraphNodeHoverTool

def graph_from_dict(d):
    """ Creates a NetworkX Graph from a dictionary
    
    Parameters
    ----------
    d : dict
    
    Returns
    -------
    Graph: NetworkX Graph
    
    Examples
    --------
    >>> g = graph_from_dict({'a':['b'], 'b':['c', 'd'], 'c':[], 'd':[], 'e':['d']})
    """
    
    g = networkx.DiGraph()
    for key, children in d.items():
        for child in children:
            g.add_edge(key, child)
    return g

class GraphView(HasTraits):
    """ View containing visualization of a networkx graph.
    """

    # The graph to be visualized
    graph = Instance(networkx.Graph)
    
    # How the graph's visualization should be layed out
    layout = Enum('spring', 'tree', 'shell', 'circular')
    
    # Scrolled contained which holds the canvas in a viewport
    _container = Instance(Scrolled)
    
    # The canvas which the graph will be drawn on
    _canvas = Instance(GraphContainer)

    traits_view = View(Item('_container', editor=ComponentEditor(),
                            show_label=False),
                        width=400,
                        height=400,
                        resizable=True)
    
    def __canvas_default(self):
        """ default setter for _canvas
        """
        if self.graph.is_directed():
            container = DAGContainer(style=self.layout)
        else:
            container = GraphContainer(style=self.layout)
            
        container.tools.append(GraphNodeSelectionTool(component=container))
        container.tools.append(GraphNodeHoverTool(component=container,
                                                  callback=self._on_hover))
        return container
    
    def __container_default(self):
        """ default setter for _container
        """
        
        viewport = Viewport(component=self._canvas, enable_zoom=True)
        viewport.view_position = [0,0]
        viewport.tools.append(ViewportPanTool(viewport))
        
        return Scrolled(self._canvas, 
                        viewport_component = viewport)
    
    def _graph_changed(self, new):
        """ handler for changes to graph attribute
        """
        for node in new.nodes():
            # creating a component will automatically add it to the canvas
            GraphNodeComponent(container=self._canvas, value=node)
                
            
        self._canvas.graph = new

    def _layout_changed(self, new):
        self._canvas.style = new

    def _on_hover(self, label):
        print "hovering over:", label
