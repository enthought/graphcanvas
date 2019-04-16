# (C) Copyright 2009-2019 Enthought, Inc., Austin, TX
# All rights reserved.

import networkx

from traits.api import Instance

from graphcanvas.graph_container import GraphContainer


class DAGContainer(GraphContainer):
    """ Enable Container for Directed Acyclic Graphs
    """

    graph = Instance(networkx.DiGraph)
