import unittest

import mock
import networkx

from enable.testing import EnableTestAssistant
from graphcanvas.graph_node_drag_tool import GraphNodeDragTool
from graphcanvas.graph_container import GraphContainer
from graphcanvas.graph_node_component import GraphNodeComponent


class TestGraphNodeDragTool(EnableTestAssistant, unittest.TestCase):
    def setUp(self):
        g = networkx.DiGraph()
        self.container = GraphContainer(graph=g)
        self.tool = GraphNodeDragTool(component=self.container)
        self.container.tools.append(self.tool)
        self.container.components.append(
            GraphNodeComponent(position=[0, 0])
        )

    def tearDown(self):
        del self.container
        del self.tool

    def test_get_value(self):
        # is in
        self.tool.original_screen_point = (0, 0)
        result = self.tool.get_value()
        self.assertIsInstance(result, GraphNodeComponent)

        # not in
        self.tool.original_screen_point = (50, 50)
        result = self.tool.get_value()
        self.assertIsNone(result)

    def test_set_delta(self):
        delta_x = 10
        delta_y = 10
        self.tool.original_screen_point = (0, 0)
        value = self.tool.get_value()
        self.tool.set_delta(value, delta_x, delta_y)
        self.assertEqual(value.x, delta_x)
        self.assertEqual(value.y, delta_y)

    def test_dragging(self):
        mock_window = self.create_mock_window()
        mock_window.get_pointer_position = mock.Mock(return_value=(0, 0))
        self.tool.original_screen_point = (0, 0)
        self.tool.original_data_point = (0, 0)
        event = self.create_drag_event(window=mock_window)
        self.tool.dragging(event)
        mock_window.set_pointer.assert_called_once_with('hand')


if __name__ == '__main__':
    unittest.main()
