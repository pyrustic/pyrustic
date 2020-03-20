import unittest


test_loader = unittest.TestLoader()
test_suite = test_loader.discover("tests")

runner = unittest.TextTestRunner()
runner.run(test_suite)
