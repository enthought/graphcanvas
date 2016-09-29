from StringIO import StringIO
import sys
import unittest

import networkx

from enable.api import BasicEvent, Interactor
from graphcanvas.graph_node_selection_tool import GraphNodeSelectionTool
from graphcanvas.graph_container import GraphContainer
from graphcanvas.graph_node_component import GraphNodeComponent
from traits.api import HasTraits, Str
from traitsui.api import Handler


def assertable_edit_traits(self, view=None, parent=None,
                         kind=None, context=None,
                         handler= None, id= '',
                         scrollable=None, **args):
    print 'edit_traits fired'


class TraitedNodeValue(HasTraits):
    label = Str

    def edit_traits(self, view=None, parent=None,
                    kind=None, context=None,
                    handler= None, id= '',
                    scrollable=None, **args):
        print 'traited node edit_traits fired'


class TraitedNode(object):
    def __init__(self, value, position):
        self.position = position
        self.value = value

    def __str__(self):
        return self.value

    def is_in(self, event_x, event_y):
        x, y = self.position
        return all([x == event_x, y == event_y])



class UntraitedNode(object):
    def __init__(self, value, position):
        self.position = position
        self.value = value

    def __str__(self):
        return self.value

    def is_in(self, event_x, event_y):
        x, y = self.position
        return all([x == event_x, y == event_y])

    def edit_traits(self, view=None, parent=None,
                    kind=None, context=None,
                    handler= None, id= '',
                    scrollable=None, **args):
        print 'untraited edit_traits fired'


class TestGraphNodeSelectionTool(unittest.TestCase):
    def setUp(self):
        g = networkx.DiGraph()
        self.container = GraphContainer(graph=g)
        self.tool = GraphNodeSelectionTool(component=self.container)
        self.container.tools.append(self.tool)
        self.container.components.append(GraphNodeComponent(position=[0, 0]))

    def tearDown(self):
        del self.container
        del self.tool

    def test_normal_left_dclick_in(self):
        event = BasicEvent(x=0, y=0, handled=False)
        node = self.container.components[0]

        # monkey-patch edit_traits method to something testable
        original_edit_traits = GraphNodeComponent.edit_traits
        GraphNodeComponent.edit_traits = assertable_edit_traits

        stdout = sys.stdout
        sys.stdout = result = StringIO()
        self.tool.normal_left_dclick(event)
        self.assertEqual(result.getvalue(), 'edit_traits fired\n')
        sys.stdout.close()
        sys.stdout = stdout

        # put the original edit_traits method back
        GraphNodeComponent.edit_traits = original_edit_traits

    def test_normal_left_dclick_not_in(self):
        event = BasicEvent(x=50, y=50, handled=False)
        ui = self.tool.normal_left_dclick(event)
        self.assertFalse(event.handled)

    def test_untraited_node(self):
        event = BasicEvent(x=0, y=0, handled=False)
        self.container.components.pop(0)
        self.container.components.append(
            UntraitedNode('untraited_node', [0, 0])
        )
        stdout = sys.stdout
        sys.stdout = result = StringIO()
        self.tool.normal_left_dclick(event)
        self.assertEqual(result.getvalue(), 'untraited edit_traits fired\n')
        sys.stdout.close()
        sys.stdout = stdout

    def test_traited_node(self):
        event = BasicEvent(x=0, y=0, handled=False)
        self.container.components.pop(0)
        self.container.components.append(
            TraitedNode(TraitedNodeValue(label='traited_node'), [0, 0])
        )
        stdout = sys.stdout
        sys.stdout = result = StringIO()
        self.tool.normal_left_dclick(event)
        self.assertEqual(result.getvalue(), 'traited node edit_traits fired\n')
        sys.stdout.close()
        sys.stdout = stdout


if __name__ == '__main__':
    unittest.main()
