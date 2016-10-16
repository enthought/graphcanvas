import unittest

import mock
import networkx

from graphcanvas.graph_container import GraphContainer
from graphcanvas.graph_node_component import GraphNodeComponent
from graphcanvas.graph_view import graph_from_dict
from kiva.testing import KivaTestAssistant

class TestGraphContainer(KivaTestAssistant, unittest.TestCase):
    def create_graph_container(self):
        """ Utility method to generate a GraphContainer with a simple graph for
            re-use in several tests herein.
        """
        d = {'a':['b'], 'b':['c', 'd'], 'c':[], 'd':[]}
        g = graph_from_dict(d)
        container = GraphContainer(graph=g)
        for node in g.nodes():
            GraphNodeComponent(container=container, value=node)
        return container

    def assert_in_bounds(self, container):
        """ Utility method for asserting that all components are contained
            within the bounds of the container.
        """
        upper_x, upper_y = container.bounds
        lower_x, lower_y = 0, 0
        for component in container.components:
            self.assertGreaterEqual(upper_x, component.x)
            self.assertGreaterEqual(component.x, lower_x)
            self.assertGreaterEqual(upper_y, component.y)
            self.assertGreaterEqual(component.y, lower_y)

    def test_no_layout_needed(self):
        container = self.create_graph_container()
        container._graph_layout_needed = False
        result = container.do_layout()
        self.assertIsNone(result)

    def test_no_nodes(self):
        container = GraphContainer(graph=graph_from_dict({}))
        self.assertTrue(container.components == [])
        result = container.do_layout()
        self.assertIsNone(result)

    def test_do_layout(self):
        container = self.create_graph_container()
        # test spring layout
        container.style = 'spring'
        self.assertTrue(container._graph_layout_needed)
        container.do_layout()
        self.assert_in_bounds(container)
        self.assertFalse(container._graph_layout_needed)

        # test tree layout
        container = self.create_graph_container()
        container.style = 'tree'
        self.assertTrue(container._graph_layout_needed)
        container.do_layout()
        self.assert_in_bounds(container)
        self.assertFalse(container._graph_layout_needed)

        # test shell layout
        container = self.create_graph_container()
        container.style = 'shell'
        self.assertTrue(container._graph_layout_needed)
        container.do_layout()
        self.assert_in_bounds(container)
        self.assertFalse(container._graph_layout_needed)

        # test spectral layout
        container = self.create_graph_container()
        container.style = 'spectral'
        self.assertTrue(container._graph_layout_needed)
        container.do_layout()
        self.assert_in_bounds(container)
        self.assertFalse(container._graph_layout_needed)

        # test circular layout
        container = self.create_graph_container()
        container.style = 'circular'
        self.assertTrue(container._graph_layout_needed)
        container.do_layout()
        self.assert_in_bounds(container)
        self.assertFalse(container._graph_layout_needed)

    def test_draw(self):
        container = self.create_graph_container()
        self.assertPathsAreCreated(container)

    def test_draw_directed_arrow_direction(self):
        d = {'a':['b'], 'b':[]}
        g = graph_from_dict(d)
        container = GraphContainer(graph=g)
        for node in g.nodes():
            GraphNodeComponent(container=container, value=node)

        # Node a is to the left of node b
        container._layout_needed = False
        container.components[0].x = 0.0
        container.components[1].x = 100.0
        container.components[0].y = 0.0
        container.components[1].y = 0.0
        self.assertPathsAreCreated(container)

        # Node a is to the right of node b
        container._layout_needed = False
        container.components[0].x = 100.0
        container.components[1].x = 0.0
        container.components[0].y = 0.0
        container.components[1].y = 0.0
        self.assertPathsAreCreated(container)

        # Node a is above of node b
        container._layout_needed = False
        container.components[0].x = 0.0
        container.components[1].x = 0.0
        container.components[0].y = 0.0
        container.components[1].y = 100.0
        self.assertPathsAreCreated(container)

        # Node a is below of node b
        container._layout_needed = False
        container.components[0].x = 0.0
        container.components[1].x = 0.0
        container.components[0].y = 100.0
        container.components[1].y = 0.0
        self.assertPathsAreCreated(container)

    def test_draw_no_layout(self):
        container = self.create_graph_container()
        container._layout_needed = False
        self.assertPathsAreCreated(container)

    def test_draw_not_directed(self):
        d = {'a':['b'], 'b':['c', 'd'], 'c':[], 'd':[]}
        g = graph_from_dict(d)
        g = g.to_undirected()
        container = GraphContainer(graph=g)
        for node in g.nodes():
            GraphNodeComponent(container=container, value=node)
        self.assertPathsAreCreated(container)

    def test_weighted(self):
        g = networkx.Graph()
        g.add_edge('a','b',weight=0.6)
        g.add_edge('a','c',weight=0.2)
        g.add_edge('c','d',weight=0.1)
        g.add_edge('c','e',weight=0.7)
        g.add_edge('c','f',weight=0.9)
        g.add_edge('a','d',weight=0.3)
        container = GraphContainer(graph=g)
        for node in g.nodes():
            GraphNodeComponent(container=container, value=node)
        self.assertPathsAreCreated(container)

    def test_spring_layout_with_non_zero_initial_positions(self):
        container = self.create_graph_container()
        for component in container.components:
            component.position = [1.0, 2.0]
        container.style = 'spring'
        self.assertTrue(container._graph_layout_needed)
        container.do_layout()
        self.assert_in_bounds(container)
        self.assertFalse(container._graph_layout_needed)

    @mock.patch('graphcanvas.layout.tree_layout')
    @mock.patch('networkx.drawing.nx_agraph.pygraphviz_layout')
    def test_no_pygraphviz(self, mock_pygraphviz_layout, mock_tree_layout):
        mock_pygraphviz_layout.side_effect = ImportError()
        container = self.create_graph_container()
        container.style = 'tree'
        container.do_layout()
        self.assert_in_bounds(container)
        self.assertFalse(container._graph_layout_needed)
        mock_pygraphviz_layout.assert_called_once_with(
            container.graph, prog='dot'
        )


if __name__ == '__main__':
    unittest.main()
