# (C) Copyright 2010-2019 Enthought, Inc., Austin, TX
# All rights reserved.

import unittest

import mock
import networkx

from enable.api import BasicEvent
from graphcanvas.graph_node_hover_tool import GraphNodeHoverTool
from graphcanvas.graph_container import GraphContainer
from graphcanvas.graph_node_component import GraphNodeComponent


class TestGraphNodeHoverTool(unittest.TestCase):
    def setUp(self):
        g = networkx.DiGraph()
        self.container = GraphContainer(graph=g)
        self.tool = GraphNodeHoverTool(component=self.container,
                                       callback=mock.Mock())
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

    def test_normal_mouse_move(self):
        event = BasicEvent(x=10, y=10, handled=False)
        self.tool.normal_mouse_move(event)
        self.assertEqual(self.tool._last_xy, (10, 10))

    def test_on_hover(self):
        # test in
        self.tool._last_xy = (0, 0)
        self.tool.callback = mock.Mock()
        self.tool.on_hover()
        self.tool.callback.assert_called_once_with('test')

        # test not in
        self.tool._last_xy = (-100, -100)
        self.tool.callback = mock.Mock()
        self.tool.on_hover()
        self.tool.callback.assert_not_called()

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
        tool.on_hover()


if __name__ == '__main__':
    unittest.main()
