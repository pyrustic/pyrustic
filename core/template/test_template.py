data ="""
import about
import unittest


class {}(unittest.TestCase):
    
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

    def test_something(self):
        self.assertEqual(1, 0)


if __name__ == '__main__':
    unittest.main()

"""