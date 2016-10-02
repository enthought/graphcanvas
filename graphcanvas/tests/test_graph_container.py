import unittest

import mock
import networkx

from graphcanvas.graph_container import GraphContainer
from graphcanvas.graph_node_component import GraphNodeComponent
from graphcanvas.graph_view import graph_from_dict
from kiva.image import GraphicsContext

class TestGraphContainer(unittest.TestCase):
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

    def assert_components_drawn(self, container):
        """ Utility method for asserting that all components are found where
            they are expected.
        """
        for component in container.components:
            x_padding = 0
            y_padding = 0
            if component.x == 0:
                x_padding = component.padding_left
            elif component.x == container.bounds[0]:
                x_padding = -component.padding_right
            if component.y == 0:
                y_padding = component.padding_bottom
            elif component.y == container.bounds[1]:
                y_padding = -component.padding_top
            components_at_list = container.components_at(
                component.x + x_padding,
                component.y + y_padding
            )
            self.assertEqual(components_at_list, [component])

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

        # test circular layout
        container = self.create_graph_container()
        container.style = 'circular'
        self.assertTrue(container._graph_layout_needed)
        container.do_layout()
        self.assert_in_bounds(container)
        self.assertFalse(container._graph_layout_needed)

    def test_draw(self):
        container = self.create_graph_container()
        gc = GraphicsContext(tuple(container.bounds))
        # draw the contents of the container
        container.draw(gc)
        # find the expected position of each component and test that it is
        # drawn there
        self.assert_components_drawn(container)

    def test_draw_directed_arrow_direction(self):
        d = {'a':['b'], 'b':[]}
        g = graph_from_dict(d)
        container = GraphContainer(graph=g)
        for node in g.nodes():
            GraphNodeComponent(container=container, value=node)
        gc = GraphicsContext(tuple(container.bounds))

        # Node a is to the left of node b
        container._layout_needed = False
        container.components[0].x = 0.0
        container.components[1].x = 100.0
        container.draw(gc)
        self.assert_components_drawn(container)

        # Node a is to the right of node b
        container._layout_needed = False
        container.components[0].x = 100.0
        container.components[1].x = 0.0
        container.draw(gc)
        self.assert_components_drawn(container)

    def test_draw_no_layout(self):
        container = self.create_graph_container()
        gc = GraphicsContext(tuple(container.bounds))
        # set _layout_needed to False
        container._layout_needed = False
        # draw the contents of the container
        container.draw(gc)
        # test that all components are at (0, 0)
        zero_zero_list = container.components_at(0, 0)
        self.assertItemsEqual(container.components, zero_zero_list)

    def test_draw_not_directed(self):
        d = {'a':['b'], 'b':['c', 'd'], 'c':[], 'd':[]}
        g = graph_from_dict(d)
        g = g.to_undirected()
        container = GraphContainer(graph=g)
        for node in g.nodes():
            GraphNodeComponent(container=container, value=node)
        gc = GraphicsContext(tuple(container.bounds))
        container.draw(gc)
        self.assert_components_drawn(container)

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
        gc = GraphicsContext(tuple(container.bounds))

        container.draw(gc)
        self.assert_components_drawn(container)

    @mock.patch('networkx.drawing.nx_agraph.pygraphviz_layout',
                side_effect=ImportError)
    def test_no_pygraphviz(self, mock_pygraphviz_layout):
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
