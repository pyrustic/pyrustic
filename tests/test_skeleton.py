import unittest


class TestSkeleton(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_one(self):
        """ test_one """
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
