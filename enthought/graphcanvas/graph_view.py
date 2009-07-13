import networkx

from enthought.enable.api import ComponentEditor, Scrolled,Viewport
from enthought.enable.tools.api import ViewportPanTool
from enthought.traits.api import HasTraits, Instance, Dict, Any
from enthought.traits.ui.api import View, Item

from dag_container import DAGContainer
from graph_node_component import GraphNodeComponent
from graph_node_selection_tool import GraphNodeSelectionTool

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
    
    # Scrolled contained which holds the canvas in a viewport
    _container = Instance(Scrolled)
    
    # The canvas which the graph will be drawn on
    _canvas = Instance(DAGContainer)

    traits_view = View(Item('_container', editor=ComponentEditor(),
                            show_label=False),
                        width=1600,
                        height=400,
                        resizable=True)
    
    def __canvas_default(self):
        """ default setter for _canvas
        """
        container = DAGContainer()
        container.tools.append(GraphNodeSelectionTool(component=container))
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
            GraphNodeComponent(container=self._canvas, value=node,
                                  children=self.graph.successors(node))
            
        self._canvas.graph = new
                        
if __name__ == '__main__':
    from enthought.traits.api import Str
    g = graph_from_dict({'a':['b'], 'b':['c', 'd'], 'c':[], 'd':[], 'e':['d']})

    class BaseNode(HasTraits):
        pass
    
    class ExpressionNode(BaseNode):
        stmt = Str()
        
        def __str__(self):
            return self.stmt
        
    class IfNode(BaseNode):
        if_condition = Str()
        lbranch = Instance(BaseNode)
    
        def __str__(self):
            return self.if_condition
        
    class IfElseNode(IfNode):
        rbranch = Instance(BaseNode)
        
        def __str__(self):
            return self.if_condition + ": else"
                            
    success_node = ExpressionNode(stmt='horray')
    fail_node = ExpressionNode(stmt='boo')
    if_a_gt_10_else = IfElseNode(if_condition='a>10', lbranch=success_node, rbranch=fail_node)
    if_a_gt_5 = IfNode(if_condition='a>5', lbranch=if_a_gt_10_else)
#    g = Graph({if_a_gt_5:[if_a_gt_10_else], if_a_gt_10_else:[success_node, fail_node], 
#               success_node:[], fail_node:[]})

#    g = networkx.DiGraph()
#    g.add_edge(if_a_gt_5, if_a_gt_10_else)
#    g.add_edge(if_a_gt_10_else, success_node)
#    g.add_edge(if_a_gt_10_else, fail_node)

    
    GraphView(graph=g).configure_traits()
    