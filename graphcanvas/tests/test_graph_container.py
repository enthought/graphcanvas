import unittest

import networkx

from graphcanvas.graph_container import GraphContainer
from graphcanvas.graph_node_component import GraphNodeComponent
from graphcanvas.graph_view import graph_from_dict


class TestGraphContainer(unittest.TestCase):
    def create_graph_container(self):
        d = {'a':['b'], 'b':['c', 'd'], 'c':[], 'd':[]}
        g = graph_from_dict(d)
        container = GraphContainer(graph=g)
        for node in g.nodes():
            GraphNodeComponent(container=container, value=node)
        return container

    def assert_in_bounds(self, container):
        upper_x, upper_y = container.bounds
        lower_x, lower_y = (0, 0)
        for component in container.components:
            self.assertTrue(lower_x <= component.x <= upper_x)
            self.assertTrue(lower_y <= component.y <= upper_y)

    def test_do_layout(self):
        container = self.create_graph_container()
        # test spring layout
        container.style = 'spring'
        container.do_layout()
        self.assert_in_bounds(container)
        self.assertFalse(container._graph_layout_needed)

        # test tree layout
        container = self.create_graph_container()
        container.style = 'tree'
        container.do_layout()
        self.assert_in_bounds(container)
        self.assertFalse(container._graph_layout_needed)

        # test shell layout
        container = self.create_graph_container()
        container.style = 'shell'
        container.do_layout()
        self.assert_in_bounds(container)
        self.assertFalse(container._graph_layout_needed)

        # test circular layout
        container = self.create_graph_container()
        container.style = 'circular'
        container.do_layout()
        self.assert_in_bounds(container)
        self.assertFalse(container._graph_layout_needed)
