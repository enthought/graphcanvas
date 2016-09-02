import unittest

import networkx

from enable.api import Scrolled, Viewport
from enable.tools.api import ViewportPanTool, ViewportZoomTool

from graphcanvas.dag_container import DAGContainer
from graphcanvas.graph_container import GraphContainer
from graphcanvas.graph_node_selection_tool import GraphNodeSelectionTool
from graphcanvas.graph_node_hover_tool import GraphNodeHoverTool
from graphcanvas.graph_view import GraphView, graph_from_dict

class TestGraphFromDict(unittest.TestCase):

    def test_graph_from_dict(self):
        d = {'a':['b'], 'b':['c', 'd'], 'c':[], 'd':[], 'e':['d']}
        g = graph_from_dict(d)
        for key, value in d.iteritems():
            children = g.successors(key)
            expected_children = value
            self.assertListEqual(children, expected_children)

class TestGraphView(unittest.TestCase):

    def setUp(self):
        self.d = {'a':['b'], 'b':['c', 'd'], 'c':[], 'd':[], 'e':['d']}
        self.g = graph_from_dict(self.d)
        self.view = GraphView(graph=self.g, layout='spring')

    def tearDown(self):
        del self.d
        del self.g
        del self.view

    def test_canvas(self):
        self.assertIsInstance(self.view._canvas, DAGContainer)
        tools = self.view._canvas.tools
        self.assertEquals(len(tools), 2)
        self.assertIsInstance(tools[0], GraphNodeSelectionTool)
        self.assertIsInstance(tools[1], GraphNodeHoverTool)

    def test_undirected_canvas(self):
        undir_g = self.g.to_undirected()
        undir_view = GraphView(graph=undir_g)
        self.assertIsInstance(undir_view._canvas, GraphContainer)
        self.assertNotIsInstance(undir_view._canvas, DAGContainer)

    def test_container(self):
        container = self.view._container
        self.assertIsInstance(container, Scrolled)

        viewport = container.viewport_component
        self.assertIsInstance(viewport, Viewport)

        self.assertEquals(len(viewport.tools), 2)
        self.assertIsInstance(viewport.tools[0], ViewportZoomTool)
        self.assertIsInstance(viewport.tools[1], ViewportPanTool)

    def test_layout_changed(self):
        new_layout = 'circular'
        self.view.layout = new_layout
        self.assertEquals(self.view._canvas.style, new_layout)

if __name__ == '__main__':
    unittest.main()
