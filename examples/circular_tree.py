import networkx
from graphcanvas.api import GraphView

try:
    import pygraphviz
except ImportError:
    import sys
    print ''
    print 'ERROR: circular layout requires pygraphviz: '\
          'http://networkx.lanl.gov/pygraphviz'
    print ''
    sys.exit(2)

g = networkx.balanced_tree(3,5)
GraphView(graph=g, layout='circular').configure_traits()
