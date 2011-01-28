import networkx

from enthought.enable.api import Container
from enthought.traits.api import Instance, Enum

from graph_container import GraphContainer

class DAGContainer(GraphContainer):
    """ Enable Container for Directed Acyclic Graphs
    """

    graph = Instance(networkx.DiGraph)
