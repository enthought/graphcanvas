# (C) Copyright 2009-2019 Enthought, Inc., Austin, TX
# All rights reserved.

import unittest

import mock
import networkx

from enable.api import BasicEvent
from graphcanvas.graph_node_selection_tool import GraphNodeSelectionTool
from graphcanvas.graph_container import GraphContainer
from graphcanvas.graph_node_component import GraphNodeComponent
from traits.api import HasTraits, Str


class TraitedNodeValue(HasTraits):
    label = Str
    edit_traits = mock.Mock()


class TestGraphNodeSelectionTool(unittest.TestCase):
    def setUp(self):
        g = networkx.DiGraph()
        self.container = GraphContainer(graph=g)
        self.tool = GraphNodeSelectionTool(component=self.container)
        self.container.tools.append(self.tool)
        node = GraphNodeComponent(position=[0, 0])
        self.container.components.append(node)

    def tearDown(self):
        del self.container
        del self.tool

    def test_normal_left_dclick_in(self):
        event = BasicEvent(x=0, y=0, handled=False)
        node = self.container.components[0]
        node.edit_traits = mock.Mock()
        self.tool.normal_left_dclick(event)
        node.edit_traits.assert_called_once_with(kind='livemodal')

    def test_normal_left_dclick_not_in(self):
        event = BasicEvent(x=50, y=50, handled=False)
        node = self.container.components[0]
        node.edit_traits = mock.Mock()
        self.tool.normal_left_dclick(event)
        node.edit_traits.assert_not_called()
        self.assertFalse(event.handled)

    def test_traited_node(self):
        event = BasicEvent(x=0, y=0, handled=False)
        self.container.components.pop(0)
        node = GraphNodeComponent(
            value=TraitedNodeValue(label='traited_node'),
            position=[0, 0],
        )
        self.container.components.append(node)
        self.tool.normal_left_dclick(event)
        node.value.edit_traits.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
