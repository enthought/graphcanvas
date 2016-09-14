import string
import unittest

from graphcanvas.graph_node_component import GraphNodeComponent


class NodeTester(object):
    def __init__(self, label):
        self.label = label


class TestGraphNodeComponent(unittest.TestCase):
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
        self.assertEqual(len(result), 20)
        self.assertEqual(expected_label, result)

    def test__key(self):
        node = self.node
        test_value = {'key': 'value'}
        node.value = test_value
        self.assertTrue(node._key is node.value)
        self.assertTrue(node._key is test_value)


if __name__ == '__main__':
    unittest.main()
