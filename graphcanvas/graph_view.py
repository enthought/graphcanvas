from __future__ import print_function
from six import text_type

import networkx

from enable.api import ComponentEditor, Scrolled,Viewport
from enable.tools.api import ViewportPanTool
from traits.api import HasTraits, Instance, Dict, Any, Enum, \
        on_trait_change, Property, cached_property, List
from traitsui.api import View, Item

from graphcanvas.dag_container import DAGContainer
from graphcanvas.graph_container import GraphContainer, SUPPORTED_LAYOUTS
from graphcanvas.graph_node_component import GraphNodeComponent
from graphcanvas.graph_node_selection_tool import GraphNodeSelectionTool
from graphcanvas.graph_node_hover_tool import GraphNodeHoverTool
from graphcanvas.graph_node_drag_tool import GraphNodeDragTool


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
    nodes = Property(List, depends_on='graph')

    # How the graph's visualization should be layed out
    layout = Enum(SUPPORTED_LAYOUTS)

    # Scrolled contained which holds the canvas in a viewport
    _container = Instance(Scrolled)

    # The canvas which the graph will be drawn on
    _canvas = Instance(GraphContainer)

    traits_view = View(Item('_container', editor=ComponentEditor(),
                            show_label=False),
                        width=400,
                        height=400,
                        resizable=True)

    def __init__(self, *args, **kw):
        super(GraphView, self).__init__(*args, **kw)

        if isinstance(self.graph.nodes()[0], HasTraits):
            self.on_trait_change(self.node_changed, 'nodes.+')

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
        container.tools.append(GraphNodeDragTool(component=container))
        return container

    def __container_default(self):
        """ default setter for _container
        """

        viewport = Viewport(component=self._canvas, enable_zoom=True)
        viewport.view_position = [0,0]
        viewport.tools.append(ViewportPanTool(viewport))

        return Scrolled(self._canvas,
                        viewport_component = viewport)

    @cached_property
    def _get_nodes(self):
        return self.graph.nodes()

    def _graph_changed(self, new):
        """ handler for changes to graph attribute
        """

        for component in self._canvas.components:
            component.container = None

        self._canvas._components = []

        for node in new.nodes():
            # creating a component will automatically add it to the canvas
            GraphNodeComponent(container=self._canvas, value=node)

        self._canvas.graph = new
        self._canvas._graph_layout_needed = True
        self._canvas.request_redraw()

    def _layout_changed(self, new):
        self._canvas.style = new

    def _on_hover(self, label):
        print(u"hovering over: {}".format(text_type(label)))

#    @on_trait_change('nodes.+')
    def node_changed(self, name, obj, old, new):
        print(u"node changed")
        self._canvas.request_redraw()
