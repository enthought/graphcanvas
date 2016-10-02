import string
import unittest

from graphcanvas.graph_node_component import GraphNodeComponent
from kiva.testing import KivaTestAssistant


class NodeTester(object):
    def __init__(self, label):
        self.label = label


class TestGraphNodeComponent(KivaTestAssistant, unittest.TestCase):
    def setUp(self):
        self.node = GraphNodeComponent()

    def tearDown(self):
        del self.node

    def test_label(self):
        node = self.node

        # test when value has a label
        expected_label = 'test'
        node.value = NodeTester(label=expected_label)
        result = node.label
        self.assertEqual(result, expected_label)

        # test when value has no label
        node.value = {'key': 'value'}
        expected_label = "{'key': 'value'}"
        result = node.label
        self.assertEqual(result, expected_label)

        # test long label
        node.value = NodeTester(label=string.ascii_lowercase)
        expected_label = string.ascii_lowercase[:17] + '...'
        result = node.label
        self.assertEqual(expected_label, result)

    def test__key(self):
        node = self.node
        test_value = {'key': 'value'}
        node.value = test_value
        self.assertIs(node._key, node.value)
        self.assertIs(node._key, test_value)

    def test_draw(self):
        node = self.node
        node.value = NodeTester(label=string.ascii_lowercase)
        self.assertPathsAreCreated(node)


if __name__ == '__main__':
    unittest.main()
