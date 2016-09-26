import unittest

import graphcanvas.api


class TestAPI(unittest.TestCase):
    def test_imports(self):
        import_names = [
            'DAGContainer', 'GraphContainer', 'GraphNodeComponent',
            'GraphView', 'graph_from_dict',
        ]
        self.assertTrue(
            all([name in dir(graphcanvas.api) for name in import_names])
        )


if __name__ == '__main__':
    unittest.main()
