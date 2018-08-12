import unittest
import mongodb_ops
import depth_chart


class DepthChartTestCase(unittest.TestCase):

    # test connection to mongodb instance
    def test_connection(self):

        self.assertEqual(str(val), "['teams']")


if __name__ == '__main__':
    unittest.main()
