import networkx
from enthought.graphcanvas.api import GraphView

g=networkx.Graph()

g.add_edge('a','b',0.6)
g.add_edge('a','c',0.2)
g.add_edge('c','d',0.1)
g.add_edge('c','e',0.7)
g.add_edge('c','f',0.9)
g.add_edge('a','d',0.3)

GraphView(graph=g).configure_traits()
