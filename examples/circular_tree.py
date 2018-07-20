import networkx
from graphcanvas.api import GraphView


g = networkx.balanced_tree(3,5)
GraphView(graph=g, layout='circular').configure_traits()
