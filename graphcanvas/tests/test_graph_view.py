from StringIO import StringIO
import sys
import unittest

import networkx

from enable.api import Scrolled, Viewport
from enable.tools.api import ViewportPanTool, ViewportZoomTool
from traits.api import HasTraits, Str

from graphcanvas.dag_container import DAGContainer
from graphcanvas.graph_container import GraphContainer
from graphcanvas.graph_node_selection_tool import GraphNodeSelectionTool
from graphcanvas.graph_node_hover_tool import GraphNodeHoverTool
from graphcanvas.graph_view import GraphView, graph_from_dict


class DummyHasTraitsObject(HasTraits):
    label = Str


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

    def test_nodes(self):
        expected_nodes = self.g.nodes()
        view_nodes = self.view.nodes
        self.assertListEqual(expected_nodes, view_nodes)

    def test_graph_changed(self):
        d = {'a':['b'], 'b':['c', 'd'], 'c':[], 'd':[], 'e':['d']}
        g = graph_from_dict(d)
        view = GraphView(graph=g, layout='spring')
        new_d = {'f':['g'], 'g':['h', 'i', 'j'], 'h':[], 'i':[], 'j':[]}
        new_g = graph_from_dict(new_d)
        view.graph = new_g
        self.assertListEqual(view.nodes, new_g.nodes())

    def test_on_hover(self):
        expected = 'test'
        stdout = sys.stdout
        sys.stdout = result = StringIO()
        self.view._on_hover('test')
        self.assertEqual(result.getvalue(), 'hovering over: test\n')
        # put back original stdout
        sys.stdout.close()
        sys.stdout = stdout

    def test_node_changed(self):
        a = DummyHasTraitsObject(label='a')
        b = DummyHasTraitsObject(label='b')
        c = DummyHasTraitsObject(label='c')
        d = {a: [b], b: [c], c: []}
        g = graph_from_dict(d)
        view = GraphView(graph=g, layout='spring')

        stdout = sys.stdout
        sys.stdout = result = StringIO()
        a.label = 'test'
        self.assertEqual(result.getvalue(), 'node changed\n')
        sys.stdout.close()
        sys.stdout = stdout

if __name__ == '__main__':
    unittest.main()
