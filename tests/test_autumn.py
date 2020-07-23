import unittest
import time


class TestAutumn(unittest.TestCase):

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
        time.sleep(5)
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()

