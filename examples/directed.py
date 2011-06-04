import networkx
from graphcanvas.api import GraphView

g=networkx.DiGraph()

g.add_edge('a','b',weight=0.6)
g.add_edge('a','c',weight=0.2)
g.add_edge('c','d',weight=0.1)
g.add_edge('c','e',weight=0.7)
g.add_edge('c','f',weight=0.9)
g.add_edge('a','d',weight=0.3)

GraphView(graph=g).configure_traits()
