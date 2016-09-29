from StringIO import StringIO
import sys
import unittest

import networkx

from enable.api import BasicEvent
from graphcanvas.graph_node_hover_tool import GraphNodeHoverTool
from graphcanvas.graph_container import GraphContainer
from graphcanvas.graph_node_component import GraphNodeComponent


def simple_callback(label):
    print label


class TestGraphNodeHoverTool(unittest.TestCase):
    def setUp(self):
        g = networkx.DiGraph()
        self.container = GraphContainer(graph=g)
        self.tool = GraphNodeHoverTool(component=self.container,
                                       callback=simple_callback)
        self.container.tools.append(self.tool)
        self.container.components.append(
            GraphNodeComponent(position=[0, 0],
                               value='test')
        )

    def tearDown(self):
        del self.container
        del self.tool

    def test__is_in(self):
        self.assertTrue(self.tool._is_in(0, 0))
        self.assertFalse(self.tool._is_in(-100, -100))

    def test_normal_mosuse_move(self):
        event = BasicEvent(x=10, y=10, handled=False)
        self.tool.normal_mouse_move(event)
        self.assertEqual(self.tool._last_xy, (10, 10))

    def test_on_hover(self):
        # test in
        self.tool._last_xy = (0, 0)
        # capture stdout
        stdout = sys.stdout
        sys.stdout = result = StringIO()
        self.tool.on_hover()
        self.assertEqual(result.getvalue(), 'test\n')
        # put back original stdout
        sys.stdout.close()
        sys.stdout = stdout

        # test not in
        self.tool._last_xy = (-100, -100)
        # capture stdout
        stdout = sys.stdout
        sys.stdout = result = StringIO()
        self.tool.on_hover()
        self.assertEqual(result.getvalue(), '')
        # put back original stdout
        sys.stdout.close()
        sys.stdout = stdout

    def test_on_hover_no_callback(self):
        g = networkx.DiGraph()
        container = GraphContainer(graph=g)
        tool = GraphNodeHoverTool(component=container, callback=None)
        container.tools.append(tool)
        container.components.append(
            GraphNodeComponent(position=[0, 0],
                               value='test')
        )

        # test in
        tool._last_xy = (0, 0)
        # capture stdout
        stdout = sys.stdout
        sys.stdout = result = StringIO()
        tool.on_hover()
        self.assertEqual(result.getvalue(), '')
        # put back original stdout
        sys.stdout.close()
        sys.stdout = stdout


if __name__ == '__main__':
    unittest.main()
