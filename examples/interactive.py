# (C) Copyright 2010-2019 Enthought, Inc., Austin, TX
# All rights reserved.

import networkx
import random

from graphcanvas.api import GraphView
from traits.api import HasTraits, Instance, Int, Button
from traitsui.api import View, Item, InstanceEditor


class InteractiveDemo(HasTraits):
    g = Instance(networkx.Graph)
    add_button = Button('add connected node')
    graph_view = Instance(GraphView)

    _node_count = Int(0)

    traits_view = View(Item('graph_view',
                            editor=InstanceEditor(), style='custom',
                            show_label=False),
                       Item('add_button', show_label=False))

    def __init__(self, *args, **kw):
        super(InteractiveDemo, self).__init__(*args, **kw)

        for i in range(5):
            self._add_node()

    def _add_node(self):
       new_node = str(self._node_count)
       self._node_count += 1

       if self._node_count == 1:
           return
       if self._node_count == 2:
           self.g.add_edge('0', '1', weight=random.random())
           return

       conn_1 = str(random.randint(0, self._node_count-2))
       conn_2 = str(random.randint(0, self._node_count-2))

       self.g.add_edge(new_node, conn_1, weight=random.random())
       self.g.add_edge(new_node, conn_2, weight=random.random())



    def _g_default(self):
        return networkx.Graph()

    def _graph_view_default(self):
        return GraphView(graph=self.g)

    def _add_button_fired(self):
        self._add_node()

        # force the graph_view into thinking the graph
        # has changed so it will re-layout all of the nodes
        self.graph_view._graph_changed(self.g)

InteractiveDemo().configure_traits()
