import unittest

import networkx

from graphcanvas.layout import tree_layout


class TestLayout(unittest.TestCase):
    def assert_layout_positions(self, result, expected):
        result_x, result_y = result
        expected_x, expected_y = expected
        self.assertAlmostEqual(result_x, expected_x)
        self.assertAlmostEqual(result_y, expected_y)

    def test_layout(self):
        g = networkx.DiGraph()

        g.add_edge('root', 'child 1')
        g.add_edge('child 1', 'grandchild 1')
        g.add_edge('child 1', 'grandchild 2')
        g.add_edge('root', 'child 2')
        g.add_edge('child 2', 'grandchild 3')
        g.add_edge('child 2', 'grandchild 4')
        g.add_edge('child 2', 'grandchild 5')

        layout = tree_layout(g)
        self.assert_layout_positions(layout['root'], (0.5, 1.0))
        self.assert_layout_positions(layout['child 1'], (2 / 3., 0.5))
        self.assert_layout_positions(layout['child 2'], (1 / 3., 0.5))
        self.assert_layout_positions(layout['grandchild 1'], (5 / 6., 0.0))
        self.assert_layout_positions(layout['grandchild 2'], (4 / 6., 0.0))
        self.assert_layout_positions(layout['grandchild 3'], (3 / 6., 0.0))
        self.assert_layout_positions(layout['grandchild 4'], (2 / 6., 0.0))
        self.assert_layout_positions(layout['grandchild 5'], (1 / 6., 0.0))

    def test_non_2D(self):
        g = networkx.DiGraph()
        with self.assertRaisesRegexp(ValueError, 'only 2D graphs'):
            tree_layout(g, dim=1)
            tree_layout(g, dim=3)

    def test_not_directed(self):
        g = networkx.Graph()
        with self.assertRaisesRegexp(ValueError, 'directed'):
            tree_layout(g)

    def test_not_acyclic(self):
        g = networkx.DiGraph()
        g.add_edge('root', 'child')
        g.add_edge('child', 'root')
        with self.assertRaisesRegexp(ValueError, 'must not contain cycles'):
            tree_layout(g)


if __name__ == '__main__':
    unittest.main()
