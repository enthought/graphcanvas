import networkx
from graphcanvas.api import GraphView

g=networkx.DiGraph()

g.add_edge('root', 'child 1')
g.add_edge('child 1', 'grandchild 1')
g.add_edge('child 1', 'grandchild 2')
g.add_edge('root', 'child 2')
g.add_edge('child 2', 'grandchild 3')
g.add_edge('child 2', 'grandchild 4')
g.add_edge('child 2', 'grandchild 5')

GraphView(graph=g, layout='tree').configure_traits()
