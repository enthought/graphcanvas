import unittest

import networkx
import numpy.testing as nptest

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

        expected_root_x, expected_root_y = (0.5, 1.0)
        self.assertAlmostEqual(layout['root'][0], expected_root_x)
        self.assertAlmostEqual(layout['root'][1], expected_root_y)

        gc_xs = [value[0] for key, value in layout.items()
                 if key.startswith('child')]
        expected_gc_xs = [x / 3.0 for x in range(1, 3)]
        nptest.assert_almost_equal(sorted(gc_xs), expected_gc_xs)
        gc_ys = [value[1] for key, value in layout.items()
                 if key.startswith('child')]
        expected_gc_ys = [0.5] * 2
        nptest.assert_almost_equal(sorted(gc_ys), expected_gc_ys)

        gc_xs = [value[0] for key, value in layout.items()
                 if 'grandchild' in key]
        expected_gc_xs = [x / 6.0 for x in range(1, 6)]
        nptest.assert_almost_equal(sorted(gc_xs), expected_gc_xs)
        gc_ys = [value[1] for key, value in layout.items()
                 if 'grandchild' in key]
        expected_gc_ys = [0.0] * 5
        nptest.assert_almost_equal(sorted(gc_ys), expected_gc_ys)

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
