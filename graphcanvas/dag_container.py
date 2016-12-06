import networkx

from enable.api import Container
from traits.api import Instance, Enum

from graphcanvas.graph_container import GraphContainer


class DAGContainer(GraphContainer):
    """ Enable Container for Directed Acyclic Graphs
    """

    graph = Instance(networkx.DiGraph)
