import unittest


class TestAPI(unittest.TestCase):
    def test_imports(self):
        import graphcanvas.api
        import_names = [
            'DAGContainer', 'GraphContainer', 'GraphNodeComponent',
            'GraphView', 'graph_from_dict',
        ]
        # get all imports other than __items__
        dir_no_dunders = [
            name for name in dir(graphcanvas.api) if '__' not in name
        ]
        self.assertListEqual(dir_no_dunders, import_names)


if __name__ == '__main__':
    unittest.main()
